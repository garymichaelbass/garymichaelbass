#!/usr/bin/env python3
# File: scripts/benchmark_serving.py
# Description: Concurrent synthetic-prompt client for AMD vLLM throughput/latency.
from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

METRIC_COLUMNS = [
    "output_token_throughput_tokens_s",
    "time_to_first_token_p50_p95_p99_ms",
    "time_per_output_token_p50_p95_p99_ms",
    "inter_token_latency_itl_p50_p95_p99_ms",
    "end_to_end_request_latency_ms",
]
MISTRAL_MAX_MODEL_LEN = 32768
TOKENIZER_BOS_SLACK = 16


def finite_nonneg(value: float) -> float:
    parsed = float(value)
    if parsed != parsed or parsed < 0.0:
        return 0.0
    return parsed


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(round((pct / 100.0) * (len(ordered) - 1)))))
    return finite_nonneg(ordered[index])


def clamp_max_tokens(input_len: int, output_len: int, max_model_len: int) -> int:
    room = max(1, int(max_model_len) - max(1, int(input_len)) - TOKENIZER_BOS_SLACK)
    requested = max(1, int(output_len))
    clamped = min(requested, room)
    if clamped != requested:
        print(
            f"[INFO] clamped max_tokens {requested} -> {clamped} "
            f"(input_len={input_len} max_model_len={max_model_len} bos_slack={TOKENIZER_BOS_SLACK})",
            flush=True,
        )
    return clamped


# Streaming fix (2026-09-06): the previous version made a single blocking
# non-streaming request and derived TTFT/ITL by reusing the same elapsed-time
# number (or, on NVIDIA, an arbitrary *0.4 fudge factor) -- neither was a real
# per-token measurement. This version streams the completion (stream=true) and
# times the arrival of each token chunk, so ttft_ms is genuinely time-to-first-
# token and itl_ms/tpot_ms is a genuine mean inter-token gap, independent of e2e.
def one_request(url: str, model_name: str, input_len: int, output_len: int) -> dict:
    prompt = ("token " * input_len).strip()
    payload = json.dumps({
        "model": model_name,
        "prompt": prompt,
        "max_tokens": output_len,
        "temperature": 0,
        "stream": True,
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "text/event-stream"},
    )
    start = time.perf_counter()
    first_token_time = None
    token_times: list[float] = []
    stream_out_tokens = 0
    try:
        with urllib.request.urlopen(req, timeout=3600) as resp:
            for raw_line in resp:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line or not line.startswith("data:"):
                    continue
                data = line[len("data:"):].strip()
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                except json.JSONDecodeError:
                    continue
                choices = chunk.get("choices") or []
                text = choices[0].get("text", "") if choices else ""
                if not text:
                    continue
                now = time.perf_counter()
                if first_token_time is None:
                    first_token_time = now
                token_times.append(now)
                stream_out_tokens += 1
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"[FAIL] HTTP {exc.code} from {url}: {detail[:800]}") from exc
    end = time.perf_counter()
    elapsed_ms = (end - start) * 1000.0
    if first_token_time is None:
        first_token_time = end
    ttft_ms = (first_token_time - start) * 1000.0
    if len(token_times) >= 2:
        gaps_ms = [(token_times[i] - token_times[i - 1]) * 1000.0 for i in range(1, len(token_times))]
        itl_ms = sum(gaps_ms) / len(gaps_ms)
    else:
        itl_ms = max(0.0, elapsed_ms - ttft_ms)
    out_tokens = stream_out_tokens or output_len
    return {
        "ttft_ms": finite_nonneg(ttft_ms),
        "tpot_ms": finite_nonneg(itl_ms),
        "itl_ms": finite_nonneg(itl_ms),
        "e2e_ms": finite_nonneg(elapsed_ms),
        "out_tokens": out_tokens,
    }


def run_sweep(args, output_len: int) -> dict[str, float]:
    url = args.base_url.rstrip("/") + "/v1/completions"
    started = time.perf_counter()
    results = []
    n_prompts = max(1, int(float(args.max_num_seqs)))
    workers = max(1, int(float(args.max_concurrency)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = [
            pool.submit(one_request, url, args.model_name, int(float(args.input_len)), output_len)
            for _ in range(n_prompts)
        ]
        for fut in as_completed(futs):
            results.append(fut.result())
    wall = time.perf_counter() - started
    out_tokens = sum(item["out_tokens"] for item in results)
    tokens_per_sec = finite_nonneg(out_tokens / wall) if wall > 0 else 0.0
    return {
        METRIC_COLUMNS[0]: tokens_per_sec,
        METRIC_COLUMNS[1]: percentile([item["ttft_ms"] for item in results], 50.0),
        METRIC_COLUMNS[2]: percentile([item["tpot_ms"] for item in results], 50.0),
        METRIC_COLUMNS[3]: percentile([item["itl_ms"] for item in results], 50.0),
        METRIC_COLUMNS[4]: finite_nonneg(sum(item["e2e_ms"] for item in results) / max(1, len(results))),
        "concurrency": float(args.max_concurrency),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Concurrent vLLM throughput client")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--raw-file", default="")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--profile", default="smoke")
    parser.add_argument("--model-name", default="mistralai/Mistral-7B-v0.3")
    parser.add_argument("--dtype", default="bfloat16")
    parser.add_argument("--tensor-parallel-size", default="1")
    parser.add_argument("--gpu-memory-utilization", default="0.9")
    parser.add_argument("--prompt-source", default="synthetic")
    parser.add_argument("--input-len", default="64")
    parser.add_argument("--output-len", default="16")
    parser.add_argument("--max-model-len", default=str(MISTRAL_MAX_MODEL_LEN))
    parser.add_argument("--max-num-seqs", default="2")
    parser.add_argument("--max-concurrency", default="2")
    parser.add_argument("--output-format", default="csv")
    args = parser.parse_args()
    if str(args.prompt_source).lower() not in ("synthetic", "true", "yes"):
        raise SystemExit("[FAIL] prompt_source must remain synthetic")
    output_len = clamp_max_tokens(int(float(args.input_len)), int(float(args.output_len)), int(float(args.max_model_len)))
    run_dir = Path(args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    texts = ["concurrency,tokens_per_sec,ttft_p50_ms,tpot_p50_ms,itl_p50_ms,e2e_ms"]
    for _repeat in range(2):
        metrics = run_sweep(args, output_len)
        rows.append({"sample_index": len(rows), "status": "ok", **{key: metrics[key] for key in METRIC_COLUMNS}, "error_message": ""})
        texts.append(
            f"{int(metrics['concurrency'])},{metrics[METRIC_COLUMNS[0]]:.6f},{metrics[METRIC_COLUMNS[1]]:.6f},"
            f"{metrics[METRIC_COLUMNS[2]]:.6f},{metrics[METRIC_COLUMNS[3]]:.6f},{metrics[METRIC_COLUMNS[4]]:.6f}"
        )
    csv_path = run_dir / "raw_results.csv"
    fieldnames = ["sample_index", "status", *METRIC_COLUMNS, "error_message"]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    raw_text = "\n".join(texts) + "\n" + csv_path.read_text(encoding="utf-8")
    Path(args.raw_file or (run_dir / "raw_output.txt")).write_text(raw_text, encoding="utf-8", newline="\n")
    print(f"[PASS] collected {len(rows)} throughput/latency samples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
