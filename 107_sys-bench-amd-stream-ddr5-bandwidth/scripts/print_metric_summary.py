#!/usr/bin/env python3
"""Print numbered end-of-run metric lines from the workload definition.

2026-09-06 rewrite: the previous version had two independent bugs that,
combined, silently mislabeled the end-of-run summary for the large majority
of workloads (only 3 of 64 came out fully correct):

1. The "Metrics" spec text was split into per-metric fragments on every
   semicolon/comma, including ones that appear *inside* a metric's own
   parenthetical aside (e.g. "(thermal_throttle_event_count; often 0)").
   That fragmented a single 5-metric spec into 6-8 bogus pieces with
   duplicate/skipped numbers.
2. When a metric's slugified description didn't exactly match a key in the
   run's summary.json (the overwhelmingly common case, since collectors use
   short internal names like "tier"/"kind"/"step" while descriptions are
   long human-readable phrases), the code silently fell back to grabbing
   the Nth value *by raw dict position* and printing it next to the wrong
   label -- with no indication anything had gone wrong.

This version: (a) only splits at top-level punctuation (paren-aware), so an
aside inside parens never fragments the metric list; (b) tries several
honest, name-based ways to find the real value for each metric before ever
falling back to position, and even then only when it is unambiguous (the
count of still-unresolved definitions exactly equals the count of
still-unused numeric values). The name-based candidates tried, in order:

  - every key candidate named in the metric's own first top-level
    parenthetical, including slash-separated alternatives inside it
    (e.g. "(a / b)" tries both "a" and "b");
  - the full-phrase slug (legacy behavior);
  - the slug of just the text before the first parenthetical;
  - when that leading phrase itself ends in a slash-separated list sharing
    a common prefix (e.g. "IOPS p50/p95/p99"), each expansion in turn
    ("IOPS p50", "IOPS p95", "IOPS p99");
  - a couple of literal-constant idioms the spec text uses ("always 0",
    "hardcoded 1.0");
  - finally, for any metric still unresolved, a unique-prefix match tried
    against *every* candidate generated for it (a candidate slug that is an
    unambiguous prefix of exactly one still-unused real key, e.g.
    "local_numa_node_latency" -> "local_numa_node_latency_nsec").

Anything that still can't be resolved is printed as NOT FOUND rather than
guessed.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def _mask_parens(text: str) -> str:
    """Replace ';' and ',' that appear *inside* parentheses with sentinel
    tokens so a later naive split on ';'/',' never treats them as a
    metric-boundary. Restored by _unmask after splitting."""
    out = []
    depth = 0
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if depth > 0 and ch == ";":
            out.append("\x00SEMI\x00")
            continue
        if depth > 0 and ch == ",":
            out.append("\x00COMMA\x00")
            continue
        out.append(ch)
    return "".join(out)


def _unmask(text: str) -> str:
    return text.replace("\x00SEMI\x00", ";").replace("\x00COMMA\x00", ",")


def metric_items(definition: Path) -> list[tuple[str, str]]:
    fields = json.loads(definition.read_text(encoding="utf-8"))
    metrics = next(
        str(item.get("value", ""))
        for item in fields
        if item.get("field_name") == "Metrics"
    )
    masked = _mask_parens(metrics)
    parts = [_unmask(p) for p in re.split(r";\s*|,\s*(?=#\d)|\n", masked)]
    result: list[tuple[str, str]] = []
    for index, part in enumerate(parts, start=1):
        text = part.strip()
        if not text:
            continue
        match = re.match(r"^#(\d+)\s*:\s*(.*)$", text)
        number = match.group(1) if match else str(index)
        description = match.group(2).strip() if match else text
        result.append((number, description))
    return result


def column_name(description: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", description).strip("_").lower() or "value"


def normalize_key(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", str(name)).strip("_").lower()


def extract_paren_keys(description: str) -> list[str]:
    """Pull literal key candidates out of a metric description's first
    top-level parenthetical, e.g. 'Peak CPU package temperature
    (peak_cpu_temp_c)' -> ['peak_cpu_temp_c']. Stops at the first
    explanatory aside inside the parens so '(gups)' -> ['gups'] but
    '(rocblas-Gflops from 2*M*N*K/elapsed)' -> ['rocblas-Gflops'] and
    '(ttft_ms; estimated if non-streaming)' -> ['ttft_ms']. When the
    surviving text is itself a slash-separated list of alternative names,
    e.g. '(end_to_end_latency_ms / prompt_response_end_to_end_latency_msec)'
    or '(sustained_decode_throughput_under_cache_pressure_tokens_sec /
    output_token_throughput)', each alternative is returned as its own
    candidate so callers can try them in turn. As a lower-priority pool,
    also yields every comma/semicolon-separated token found anywhere in the
    full parenthetical (not just the first, cut-off fragment), so an aside
    like '(collector copies the same aggregate IOPS into iops_p50,
    iops_p95, and iops_p99)' still surfaces 'iops_p50', 'iops_p95', and
    'iops_p99' as candidates even though the primary cut lands on
    non-key prose."""
    match = re.search(r"\(([^()]*)\)", description)
    if not match:
        return []
    inner = match.group(1)
    cut = re.split(r";|,| from | when | if | equals | still |=", inner, maxsplit=1)
    candidate = cut[0].strip()
    primary: list[str] = []
    if candidate:
        if "/" in candidate:
            primary = [p.strip() for p in candidate.split("/") if p.strip()]
        else:
            primary = [candidate]

    extra: list[str] = []
    for token in re.split(r"[;,]", inner):
        token = re.sub(r"^\s*(and|or)\s+", "", token.strip(), flags=re.IGNORECASE)
        token = re.split(r" from | when | if | equals | still |=", token, maxsplit=1)[0].strip()
        if token and token not in primary:
            extra.append(token)

    return primary + extra


def phrase_before_paren(description: str) -> str | None:
    """The human-readable phrase preceding the first parenthetical, e.g.
    'TLB miss rate (always 0)' -> 'TLB miss rate' -> slug 'tlb_miss_rate',
    which is often the collector's real column name even when the
    parenthetical itself holds an aside rather than a key."""
    idx = description.find("(")
    if idx <= 0:
        return None
    return description[:idx].strip() or None


def distribute_slash_list(phrase: str) -> list[str]:
    """A phrase like 'IOPS p50/p95/p99' names three related metrics that
    share a common leading label, one per slash-separated token. Expand it
    into ['IOPS p50', 'IOPS p95', 'IOPS p99'] so each can be tried as its
    own candidate name. Only fires when there are at least two tokens after
    the last space before the slash list and every token looks like a short
    identifier fragment (not a full alternate phrase, which is already
    handled by extract_paren_keys' own '/' split)."""
    match = re.match(r"^(.*\s)?([A-Za-z0-9_.]+(?:/[A-Za-z0-9_.]+)+)$", phrase.strip())
    if not match:
        return []
    prefix = (match.group(1) or "").strip()
    tokens = match.group(2).split("/")
    if len(tokens) < 2:
        return []
    if not prefix:
        return []
    return [f"{prefix} {tok}".strip() for tok in tokens]


def extract_constant(description: str) -> float | None:
    """Recognize the small set of literal-constant idioms this spec text
    uses when a metric is a known, deliberately-fixed value rather than
    something computed per run (e.g. 'always 0', 'hardcoded 1.0')."""
    if re.search(r"\balways\s+0\b", description, re.IGNORECASE):
        return 0.0
    match = re.search(r"hardcoded\s+([0-9.eE+-]+)", description, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None


def _unique_prefix_match(slug: str, remaining_keys: list[str]) -> str | None:
    """If exactly one still-unused real key starts with '<slug>_', return it.
    Catches near-misses like candidate 'local_numa_node_latency' against
    real key 'local_numa_node_latency_nsec', or 'tcp_throughput' against
    'tcp_throughput_gb_s' -- fires only when unambiguous."""
    if not slug:
        return None
    prefix = slug + "_"
    matches = [k for k in remaining_keys if normalize_key(k).startswith(prefix)]
    if len(matches) == 1:
        return matches[0]
    return None


def _build_candidates(description: str) -> list[str]:
    """All the honest name candidates worth trying for one metric
    description, most-specific first."""
    candidates: list[str] = list(extract_paren_keys(description))
    candidates.append(description)  # full-phrase slug (legacy behavior)
    before = phrase_before_paren(description)
    if before:
        candidates.append(before)
        candidates.extend(distribute_slash_list(before))
    else:
        candidates.extend(distribute_slash_list(description))
    # de-duplicate while preserving order
    seen: set[str] = set()
    ordered: list[str] = []
    for c in candidates:
        if c and c not in seen:
            seen.add(c)
            ordered.append(c)
    return ordered


def resolve_metrics(items: list[tuple[str, str]], metrics: dict) -> list[tuple[str, str, object]]:
    """Return, for each (number, description) in items, a (label, value)
    resolved as honestly as possible. Never reuses the same dict key for two
    different metrics, and never guesses a value across a position mismatch."""
    norm_lookup: dict[str, str] = {}
    for key in metrics:
        norm_lookup.setdefault(normalize_key(key), key)

    used_keys: set[str] = set()
    resolved: dict[int, tuple[str, object]] = {}
    unresolved_idx: list[int] = []
    candidates_by_idx: dict[int, list[str]] = {}

    for idx, (_number, description) in enumerate(items):
        candidates = _build_candidates(description)
        candidates_by_idx[idx] = candidates
        found_key = None
        for candidate in candidates:
            key = norm_lookup.get(normalize_key(candidate))
            if key is not None and key not in used_keys:
                found_key = key
                break
        if found_key is not None:
            used_keys.add(found_key)
            resolved[idx] = (found_key, metrics[found_key])
            continue
        constant = extract_constant(description)
        if constant is not None:
            resolved[idx] = (column_name(description), constant)
            continue
        unresolved_idx.append(idx)

    # Unique-prefix-match pass: try every candidate generated for a still-
    # unresolved metric (not just the first), and only accept a match when
    # exactly one unused real key is an unambiguous extension of it.
    still_unresolved = set(unresolved_idx)
    for idx in list(unresolved_idx):
        if idx not in still_unresolved:
            continue
        for candidate in candidates_by_idx.get(idx, []):
            remaining_keys = [k for k in metrics if k not in used_keys and metrics[k] is not None]
            match = _unique_prefix_match(normalize_key(candidate), remaining_keys)
            if match is not None:
                used_keys.add(match)
                resolved[idx] = (match, metrics[match])
                still_unresolved.discard(idx)
                break
    unresolved_idx = [idx for idx in unresolved_idx if idx in still_unresolved]

    # Last resort: position-match only when it is unambiguous -- exactly as
    # many still-unresolved definitions as still-unused *numeric* values.
    remaining_keys = [k for k in metrics if k not in used_keys and metrics[k] is not None]
    if unresolved_idx and len(unresolved_idx) == len(remaining_keys):
        for idx, key in zip(unresolved_idx, remaining_keys):
            resolved[idx] = (key, metrics[key])
        unresolved_idx = []

    output = []
    for idx, (number, description) in enumerate(items):
        if idx in resolved:
            label, value = resolved[idx]
        else:
            label, value = column_name(description), "NOT FOUND"
        output.append((number, description, label, value))
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--definition", type=Path, default=Path("benchmark_specification.json"))
    parser.add_argument("--summary", type=Path, default=Path("results/summary.json"))
    args = parser.parse_args()

    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    metrics = summary.get("metrics", {})
    if not isinstance(metrics, dict):
        metrics = {}

    items = metric_items(args.definition)
    for number, description, label, value in resolve_metrics(items, metrics):
        print(f"[INFO] #{number}: {description}; {label}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
