#!/usr/bin/env python3
"""Fill self-check gaps from resolved component contracts after init/config generation."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
import sys

if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from resolve_implementation_components import (  # noqa: E402
    definition_fields,
    resolve_components,
    validate_component_vs_spec,
    validate_overlay_conflicts,
)


def _write_lf(path: Path, text: str, exe: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = text.replace("\r\n", "\n").replace("\r", "\n")
    if not data.endswith("\n"):
        data += "\n"
    path.write_bytes(data.encode("utf-8"))
    if exe or path.suffix == ".sh":
        path.chmod(path.stat().st_mode | 0o111)


def _load_gate(component_root: Path) -> dict:
    path = component_root / "gate.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _ensure_requirements(repo: Path, resolved: list[dict] | None = None) -> None:
    path = repo / "requirements.txt"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    extras = ["PyYAML>=6.0"]
    ids = {str(item.get("component_id") or "") for item in (resolved or [])}
    if ids & {"sglang-prompt-response-amd", "sglang-serving-amd"}:
        extras.extend(
            [
                "soundfile>=0.12",
                "jsonschema>=4.0",
                "numpy>=1.26",
                "python-multipart>=0.0.9",
            ]
        )
    needed = [line for line in extras if line.split(">", 1)[0].split("=", 1)[0] not in text]
    if needed:
        _write_lf(path, (text.rstrip() + "\n" if text.strip() else "") + "\n".join(needed) + "\n")


_THRESHOLDS_KEY_RE = re.compile(r"(?m)^thresholds\s*:")


def _ensure_thresholds(repo: Path, resolved: list[dict]) -> None:
    yaml_path = repo / "config" / "benchmark_config.yaml"
    if not yaml_path.is_file():
        return
    overlay_rel = "config/benchmark_config.yaml"
    if any(overlay_rel in (item["component"].get("overlay") or []) for item in resolved):
        # A resolved component already claims this exact path as one of its
        # locked overlay files. _write_overlay_lock() (below) hashes the
        # pristine source file for that lock entry; appending a thresholds
        # block here would make the repo's copy diverge from that hash, and
        # self_check would then report "locked overlay rewritten". A
        # component that owns this file is responsible for its own
        # thresholds (via gate.json, baked into the overlay file itself).
        return
    text = yaml_path.read_text(encoding="utf-8")
    if _THRESHOLDS_KEY_RE.search(text):
        # A real top-level `thresholds:` key already exists. (A bare
        # substring check here previously also matched the word appearing
        # inside a comment, which silently skipped real injection.)
        return
    thresholds: dict[str, object] = {}
    for item in resolved:
        gate = _load_gate(Path(item["component_root"]))
        thresholds.update(gate.get("thresholds") or {})
    if not thresholds:
        return
    lines = ["", "thresholds:"]
    for key, value in thresholds.items():
        lines.append(f"  {key}: {value}")
    _write_lf(yaml_path, text.rstrip() + "\n" + "\n".join(lines) + "\n")


def _ensure_seed_fixture(repo: Path) -> None:
    path = repo / "scripts" / "validate_results.py"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    if "--seed-fixture" in text:
        return
    helper = '''
def seed_fixture(config_path: Path) -> Path:
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    fixture = Path("tests/fixtures/benchmark.db")
    fixture.parent.mkdir(parents=True, exist_ok=True)
    if fixture.exists():
        fixture.unlink()
    conn = sqlite3.connect(fixture)
    conn.execute("""CREATE TABLE runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            benchmark_id TEXT, benchmark_name TEXT, status TEXT,
            started_at TEXT, finished_at TEXT, error_message TEXT)""")
    conn.execute("""CREATE TABLE samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT, run_id INTEGER,
            sample_index INTEGER, status TEXT, error_message TEXT)""")
    conn.execute(
        "INSERT INTO runs (benchmark_id, benchmark_name, status, started_at, finished_at, error_message) VALUES (?, ?, 'ok', ?, ?, NULL)",
        ("fixture", "seed-fixture", now, now),
    )
    run_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    for index in range(2):
        conn.execute(
            "INSERT INTO samples (run_id, sample_index, status, error_message) VALUES (?, ?, 'ok', NULL)",
            (run_id, index),
        )
    conn.commit()
    conn.close()
    return fixture

'''
    if "from datetime import datetime" not in text:
        text = text.replace("from pathlib import Path", "from datetime import datetime\nfrom pathlib import Path")
    text = text.replace(
        'parser.add_argument("--quiet", action="store_true")\n    args = parser.parse_args()',
        'parser.add_argument("--quiet", action="store_true")\n    parser.add_argument("--seed-fixture", action="store_true")\n    args = parser.parse_args()\n    if args.seed_fixture:\n        args.db = str(seed_fixture(Path(args.config)))',
    )
    if "def seed_fixture" not in text:
        text = text.replace("def main() -> int:", helper + "def main() -> int:")
    _write_lf(path, text, exe=True)


def _write_overlay_lock(repo: Path, resolved: list[dict]) -> None:
    lock = {}
    for item in resolved:
        cid = str(item["component_id"])
        root = Path(item["component_root"])
        for rel in item["component"].get("overlay") or []:
            src = root / "files" / str(rel)
            digest = hashlib.sha256(src.read_bytes()).hexdigest()
            lock[str(rel)] = {"component_id": cid, "sha256": digest}
    _write_lf(repo / "results" / "overlay_lock.json", json.dumps(lock, indent=2) + "\n")


def _write_resolution_report(repo: Path, resolved: list[dict], fields: dict[str, str]) -> None:
    errors, warnings = validate_component_vs_spec(fields, resolved)
    locked = []
    materialize_filled = []
    agent_may_edit = [
        "PRD.md",
        "SPEC.md",
        "README.md",
        "requirements.txt",
        "config/benchmark_config.yaml",
        "GENERATION_REPORT.md",
    ]
    for item in resolved:
        cid = str(item["component_id"])
        for rel in item["component"].get("overlay") or []:
            locked.append(f"{cid}:{rel}")
        gate = _load_gate(Path(item["component_root"]))
        if gate.get("agent_may_edit"):
            agent_may_edit = list(dict.fromkeys(agent_may_edit + list(gate["agent_may_edit"])))
        if str(item["component"].get("role")) == "mixin":
            materialize_filled.extend(str(rel) for rel in item["component"].get("overlay") or [])
    payload = {
        "implementation_component_resolution": "automatic",
        "discovered": [
            {
                "component_id": item["component_id"],
                "role": item["component"].get("role"),
                "completeness": item["component"].get("completeness"),
                "reasons": item["reasons"],
                "overlay": item["component"].get("overlay"),
                "provides": item["component"].get("provides"),
                "does_not_provide": item["component"].get("does_not_provide"),
                "contracts": item["component"].get("contracts"),
            }
            for item in resolved
        ],
        "overlay_locked": locked,
        "mixin_or_materialized": materialize_filled,
        "agent_may_edit": agent_may_edit,
        "spec_warnings": warnings,
        "spec_errors": errors,
        "collector_present": _collector_present(repo, resolved),
        "collector_entry_points": _collector_entry_points(resolved),
    }
    _write_lf(repo / "results" / "component_resolution.json", json.dumps(payload, indent=2) + "\n")
    lines = [
        "# Component resolution leftover work",
        "",
        "Locked overlay files (do not rewrite):",
    ]
    lines.extend(f"- `{item}`" for item in locked or ["(none)"])
    lines.extend(["", "Mixin / materialized files:", ""])
    lines.extend(f"- `{item}`" for item in materialize_filled or ["(none)"])
    lines.extend(["", "Agent may edit:", ""])
    lines.extend(f"- `{item}`" for item in agent_may_edit)
    entry_points = _collector_entry_points(resolved)
    if entry_points:
        lines.extend(["", "Collector entry points:", ""])
        lines.extend(f"- `{item}`" for item in entry_points)
    elif not (repo / "scripts" / "collect_workload.py").is_file():
        lines.extend(
            [
                "",
                "**No implementation-component collector matched.** Implement the measurement entry point from the benchmark specification. Do not invent a generic collector in the template.",
            ]
        )
    for warning in warnings:
        lines.append(f"- WARN: {warning}")
    _write_lf(repo / "results" / "component_leftover_work.md", "\n".join(lines) + "\n")
    print("[INFO] Wrote results/component_resolution.json and results/overlay_lock.json")
    if payload["collector_present"]:
        print("[INFO] Collector entry points:", ", ".join(payload.get("collector_entry_points") or []))
    else:
        print("[WARN] No implementation-component collector; agent must implement the measurement entry point.")


def _collector_entry_points(resolved: list[dict]) -> list[str]:
    rows: list[str] = []
    for item in resolved:
        component = item.get("component") or {}
        if str(component.get("role")) == "mixin":
            continue
        entry = str(component.get("entry_point") or "").strip()
        cid = str(item.get("component_id") or "")
        if entry:
            rows.append(f"{cid}:{entry}")
    return rows


def _collector_present(repo: Path, resolved: list[dict]) -> bool:
    for item in _collector_entry_points(resolved):
        rel = item.split(":", 1)[-1]
        if (repo / rel).is_file() and (repo / rel).stat().st_size > 0:
            return True
    collect = repo / "scripts" / "collect_workload.py"
    return collect.is_file() and collect.stat().st_size > 0


def apply_component_gaps(repo_root: Path, components_root: Path | None = None) -> int:
    repo = Path(repo_root).resolve()
    spec = repo / "benchmark_specification.json"
    if components_root is None:
        copy_name = ""
        manifest = repo / "results" / "generation_manifest.json"
        if manifest.is_file():
            copy_name = str(json.loads(manifest.read_text(encoding="utf-8")).get("template_copy_path") or "")
        if copy_name and (repo / copy_name / "implementation_components").is_dir():
            components_root = repo / copy_name / "implementation_components"
        else:
            components_root = Path(__file__).resolve().parents[1] / "implementation_components"
    try:
        resolved = resolve_components(spec, Path(components_root))
    except ValueError as exc:
        print(f"[FAIL] {exc}")
        return 1
    validate_overlay_conflicts(resolved)
    fields = definition_fields(spec)
    errors, warnings = validate_component_vs_spec(fields, resolved)
    for warning in warnings:
        print(f"[WARN] {warning}")
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    _ensure_requirements(repo, resolved)
    _ensure_thresholds(repo, resolved)
    _ensure_seed_fixture(repo)
    _write_overlay_lock(repo, resolved)
    _write_resolution_report(repo, resolved, fields)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply component contract gaps to a generated repository")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--components-root", default="")
    args = parser.parse_args()
    components = Path(args.components_root) if args.components_root else None
    return apply_component_gaps(Path(args.repo_root), components)


if __name__ == "__main__":
    raise SystemExit(main())
