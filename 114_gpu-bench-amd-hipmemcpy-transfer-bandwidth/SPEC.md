# SPEC.md: "The Human How"; Exact technical requirements, environment setup, implementation details, etc.


## Execution Description

Builds and runs bin/hip_memcpy_bw over yaml transfer sizes and directions. direction, pinned_memory, min_bytes, max_bytes, step_factor, warmup_iters, and num_iterations are forwarded when non-empty. output_format: csv Profile values are taken from `Parameters_SmokeBaselineExtend` and written to `config/benchmark_config.yaml`. Discovered implementation components: hipmemcpy-bandwidth-amd, harness-self-check.


## Parameters

| Parameter | CLI Flag | Tested Values | Default | Description |
|---|---|---|---|---|
| device_id | --device-id | 0 (smoke/baseline/extended) | 0 | Profile parameter `device_id` from yaml |
| direction | --direction | all (smoke/baseline/extended) | all | Profile parameter `direction` from yaml |
| pinned_memory | --pinned-memory | true (smoke/baseline/extended) | true | Profile parameter `pinned_memory` from yaml |
| min_bytes | --min-bytes | 1024 (smoke/baseline/extended) | 1024 | Profile parameter `min_bytes` from yaml |
| max_bytes | --max-bytes | 4096 (smoke/baseline/extended) | 4096 | VM 2026-08-16 max_bytes=1GiB num_iterations=2600 -> 206s (3:26). Extended 7500 iters ~10:00, not tested. |
| step_factor | --step-factor | 2 (smoke/baseline/extended) | 2 | Profile parameter `step_factor` from yaml |
| warmup_iters | --warmup-iters | 1 (smoke/baseline/extended) | 1 | Profile parameter `warmup_iters` from yaml |
| num_iterations | --num-iterations | 3 (smoke/baseline/extended) | 3 | VM 2026-08-16 max_bytes=1GiB num_iterations=2600 -> 206s (3:26). Extended 7500 iters ~10:00, not tested. Retimed 2026-08-17 toward 3-4 min baseline; extended scaled by the same factor. |


## Invocation

```bash
bash run_benchmark.sh --profile smoke --validate --device-id 0 --direction all --pinned-memory true --min-bytes 1024 --max-bytes 4096 --step-factor 2 --warmup-iters 1 --num-iterations 3
```


## Raw Output Format

binary stdout plus a CSV row per direction and size

```text
sample_index,status,direction,pinned_memory,transfer_size_bytes,latency_us,bandwidth_GBps,error_message
0,ok,H2D,1,1048576,12.0,18.5,
```


## Metrics

1. **Transfer bandwidth, combined H2D/D2H** — captured from collector output — stored as `bandwidth_gbps` in `samples`.
2. **Transfer latency** — captured from collector output — stored as `latency_us` in `samples`.
3. **H2D bandwidth at max size (bandwidth_gbps_h2d** — captured from collector output — stored as `h2d_bandwidth_at_max_size_bandwidth_gbps_h2d` in `samples`.


## Framework

| Component | Role |
|---|---|
| Bash | Required Framework inventory item |
| SQLite | Required Framework inventory item |
| Python | Required Framework inventory item |
| PyYAML | Required Framework inventory item |
| ROCm Runtime | Required Framework inventory item |
| C/C++ | Required Framework inventory item |
| HIP/ROCm | Required Framework inventory item |
| HIPCC | Required Framework inventory item |


## Installation and Execution Summary

Compile and run bin/hip_memcpy_bw with yaml direction, pinned_memory, min_bytes, max_bytes, step_factor, and iteration counts, then parse one row per direction and transfer size, to measure HIP copy bandwidth and latency


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
5. All required aggregate metrics are physically sensible (positive values). Per-sample `bandwidth_gbps`, `latency_us`, `h2d_bandwidth_at_max_size_bandwidth_gbps_h2d` columns are finite for every row.
6. At least 2 sample rows exist for the latest `run_id` (sweep coverage).
7. No sample has `status = 'error'`.

### Baseline / Threshold configuration (`config/benchmark_config.yaml`)

```yaml
baselines: {}
  # TBD — no published reference provided
```

Threshold key suffixes encode comparison direction when `thresholds:` is present: `_min` → observed value must be ≥ threshold. `_max` → observed value must be ≤ threshold. Informational `baselines:` ranges are not pass/fail gates. Parameters in play: `device_id`, `direction`, `pinned_memory`, `min_bytes`, `max_bytes`, `step_factor`, `warmup_iters`, `num_iterations`.
