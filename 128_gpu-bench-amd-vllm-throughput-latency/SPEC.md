# SPEC.md: "The Human How"; Exact technical requirements, environment setup, implementation details, etc.


## Execution Description

Same server split as 127 (tiny_kv smoke / vLLM bfloat16 baseline-extended on port 8000). Prompt count comes from yaml max_num_seqs; concurrency from max_concurrency. output_len is long on baseline/extended (18600 / 37200 class) and is clamped to max_model_len. output_format: csv Profile values are taken from `Parameters_SmokeBaselineExtend` and written to `config/benchmark_config.yaml`. Discovered implementation components: vllm-throughput-amd, harness-self-check.


## Parameters

| Parameter | CLI Flag | Tested Values | Default | Description |
|---|---|---|---|---|
| model_name | --model-name | mistralai/Mistral-7B-v0.3 (smoke/baseline/extended) | mistralai/Mistral-7B-v0.3 | Profile parameter `model_name` from yaml |
| dtype | --dtype | bfloat16 (smoke/baseline/extended) | bfloat16 | vLLM 0.26 rejects bf16; use bfloat16 |
| tensor_parallel_size | --tensor-parallel-size | 1 (smoke/baseline/extended) | 1 | Profile parameter `tensor_parallel_size` from yaml |
| gpu_memory_utilization | --gpu-memory-utilization | 0.9 (smoke/baseline/extended) | 0.9 | Profile parameter `gpu_memory_utilization` from yaml |
| prompt_source | --prompt-source | synthetic (smoke/baseline/extended) | synthetic | Profile parameter `prompt_source` from yaml |
| input_len | --input-len | 64 (smoke/baseline/extended) | 64 | Profile parameter `input_len` from yaml |
| output_len | --output-len | 16 (smoke/baseline/extended) | 16 | 00_78: 37200 extended was 23:05. 2026-09-08: 18600 extended measured 74:43 on a throughput-collapsed run (16-wide max_num_seqs drops batching to 1-2 concurrent sequences); the healthy-batching baseline for that token count is 23:05. Extended lowered to 16500 to retarget ~12 min. Do not push back toward 37200 -- that hits the 32768 context cap and is what produced the 23-75 min runs. |
| max_num_seqs | --max-num-seqs | 2 (smoke/baseline/extended) | 2 | Profile parameter `max_num_seqs` from yaml |
| max_concurrency | --max-concurrency | 2 (smoke/baseline/extended) | 2 | Profile parameter `max_concurrency` from yaml |


## Invocation

```bash
bash run_benchmark.sh --profile smoke --validate --model-name mistralai/Mistral-7B-v0.3 --dtype bfloat16 --tensor-parallel-size 1 --gpu-memory-utilization 0.9 --prompt-source synthetic --input-len 64 --output-len 16 --max-num-seqs 2 --max-concurrency 2
```


## Raw Output Format

raw_results.csv plus serving-client stdout. Parse raw_results.csv

```text
sample_index,status,output_token_throughput_tokens_s,time_to_first_token_p50_p95_p99_ms,time_per_output_token_p50_p95_p99_ms,inter_token_latency_itl_p50_p95_p99_ms,end_to_end_request_latency_ms,error_message
```


## Metrics

1. **Output token throughput** — captured from collector output — stored as `tokens_per_sec` in `samples`.
2. **Time To First Token, ms** — captured from collector output — stored as `ttft_p50_ms` in `samples`.
3. **Time Per Output Token, ms** — captured from collector output — stored as `tpot_p50_ms` in `samples`.
4. **Inter-token latency, ms** — captured from collector output — stored as `itl_p50_ms` in `samples`.
5. **End-to-end request latency (e2e_ms** — captured from collector output — stored as `end_to_end_request_latency_e2e_ms` in `samples`.


## Framework

| Component | Role |
|---|---|
| Bash | Required Framework inventory item |
| SQLite | Required Framework inventory item |
| Python | Required Framework inventory item |
| PyYAML | Required Framework inventory item |
| ROCm Runtime | Required Framework inventory item |
| PyTorch-ROCm | Required Framework inventory item |
| Hugging Face Transformers | Required Framework inventory item |
| vLLM | Required Framework inventory item |
| Mistral-7B-v0.3 | Required Framework inventory item |


## Installation and Execution Summary

Launch tiny_kv_server.py or python -m vllm.entrypoints.openai.api_server --dtype bfloat16 on 127.0.0.1:8000, wait for /v1/models, run concurrent benchmark_serving.py completions with yaml input_len/output_len/max_concurrency, and write throughput plus TTFT/TPOT/ITL/E2E columns to raw_results.csv, to measure vLLM serving performance


## Platform Portability

- **AMD (primary):** gfx942, ROCm 7.2.1, Framework tools listed above.
- **NVIDIA:** This is an AMD ROCm workload. An NVIDIA counterpart would use CUDA/DCGM tooling rather than the ROCm probes listed in Framework.


## Model Context Protocols

- **Active:** —


## Execution-Loop Validation Contract

EXECUTION CHAIN: `run_benchmark.sh` ➔ raw output ➔ `scripts/parse_results.py` ➔ `results/benchmark.db` ➔ `scripts/validate_results.py`

This benchmark uses a lightweight, SQLite-integrated execution loop for result validation. All validation is performed by `scripts/validate_results.py`.

### Validation script usage

```bash
export BENCHMARK_PYTHON=/usr/bin/python3.13  # optional; select the installed interpreter

# After a live run:
".venv/bin/python" scripts/validate_results.py --db results/benchmark.db

# CI / no-GPU path (seeds fixture and validates it):
".venv/bin/python" scripts/validate_results.py --seed-fixture --quiet

# Override DB path via environment variable:
BENCHMARK_DB=tests/fixtures/benchmark.db \
  ".venv/bin/python" scripts/validate_results.py
```

### Run artifact contract

Each execution writes `results/raw/YYYYMMDD_HHMMSS_<repo_name>_<hostname>/`. Required artifacts: `run.log` (full transcript with ANSI stripped in file), `commands_executed.sh` (replayable command log), masked `env_variables.txt`, `journal_warnings.txt` (`journalctl -p warning`, run-window scoped), `script.sh` (executed harness copy), raw output text, dual raw exports (`raw_results.csv`, `raw_results.jsonl`), per-run sample exports in CSV/JSON, and Excel-sourced `hardware_info.txt`, `software_info.txt`, and `errors_info.txt` in that same per-run directory. Do not write `system_info.txt`.

`run_benchmark.sh` supports resumable phase execution. Accepted forms are `--phase phase3`, `--phase 3`, and `--phase3` (same for phases 1, 2, and 4). `--raw-file <path>` points at an existing raw file for parse-only `--phase3` recovery; it is not an output-log path. `bash run_benchmark.sh --help` prints the `usage()` page and exits before setup. `bash run_benchmark.sh --matrix-definition` prints this workload's `benchmark_specification.json` field/value table and exits before setup.

### Required integrity checks (built into `validate_results.py`)

1. Latest run exists and `runs.status = 'ok'`.
2. `run.error_message` is NULL.
3. `started_at` and `finished_at` are valid ISO-8601 UTC strings.
4. All required aggregate metrics in `runs` are non-NULL and finite.
5. All required aggregate metrics are physically sensible (positive values). Per-sample `tokens_per_sec`, `ttft_p50_ms`, `tpot_p50_ms`, `itl_p50_ms`, `end_to_end_request_latency_e2e_ms` columns are finite for every row.
6. At least 2 sample rows exist for the latest `run_id` (sweep coverage).
7. No sample has `status = 'error'`.

### Baseline / Threshold configuration (`config/benchmark_config.yaml`)

```yaml
baselines: {}
  # TBD — no published reference provided
```

Threshold key suffixes encode comparison direction when `thresholds:` is present: `_min` → observed value must be ≥ threshold. `_max` → observed value must be ≤ threshold. Informational `baselines:` ranges are not pass/fail gates. Parameters in play: `model_name`, `dtype`, `tensor_parallel_size`, `gpu_memory_utilization`, `prompt_source`, `input_len`, `output_len`, `max_num_seqs`, `max_concurrency`.
