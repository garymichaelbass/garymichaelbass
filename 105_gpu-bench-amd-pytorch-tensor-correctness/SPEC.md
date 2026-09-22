# SPEC.md: "The Human How"; Exact technical requirements, environment setup, implementation details, etc.


## Execution Description

Compares GPU PyTorch matmul/conv2d against a CPU FP32 reference for each yaml op/dtype/shape. op_name: matmul or conv2d. dtype and shape: sweep values. rtol/atol: comparison gates (defaults 0.02 / 0.1). num_iterations: randomized inputs per case. seed and device_id: RNG and cuda:N. This is not pytest test_ops.py Profile values are taken from `Parameters_SmokeBaselineExtend` and written to `config/benchmark_config.yaml`. Discovered implementation components: pytorch-tensor-correctness-amd, harness-self-check.


## Parameters

| Parameter | CLI Flag | Tested Values | Default | Description |
|---|---|---|---|---|
| device_id | --device-id | 0 (smoke/baseline/extended) | 0 | Profile parameter `device_id` from yaml |
| op_name | --op-name | matmul,conv2d (smoke/baseline/extended) | matmul,conv2d | Sweep/list value. Command-column flags are documentary; omit this flag so yaml expands cases |
| dtype | --dtype | f16_r (smoke/baseline/extended) | f16_r | Sweep/list value. Command-column flags are documentary; omit this flag so yaml expands cases |
| shape | --shape | matmul=1x128x128;conv2d=1x3x32x32 (smoke/baseline/extended) | matmul=1x128x128;conv2d=1x3x32x32 | Sweep/list value. Command-column flags are documentary; omit this flag so yaml expands cases |
| rtol | --rtol | 0.02 (smoke/baseline/extended) | 0.02 | Sweep/list value. Command-column flags are documentary; omit this flag so yaml expands cases |
| atol | --atol | 0.1 (smoke/baseline/extended) | 0.1 | Sweep/list value. Command-column flags are documentary; omit this flag so yaml expands cases |
| num_iterations | --num-iterations | 2 (smoke/baseline/extended) | 2 | VM 2026-08-16 num_iterations=700 -> 187s (3:07). Extended 2250 extrapolated ~10:00, not tested. |
| seed | --seed | 42 (smoke/baseline/extended) | 42 | Profile parameter `seed` from yaml |


## Invocation

```bash
bash run_benchmark.sh --profile smoke --validate --device-id 0 --num-iterations 2 --seed 42
```


## Raw Output Format

CSV with one row per op/dtype/shape case

```text
sample_index,status,op_name,dtype,shape,max_abs_error,max_rel_error,tolerance_compliance,coverage_count,failure_count,error_message
0,ok,matmul,fp32,1x128x128,1.2e-4,8e-6,1,1,0,
```


## Metrics

1. **Max absolute error across correctness cases** — captured from collector output — stored as `max_abs_error` in `samples`.
2. **Max relative error across correctness cases** — captured from collector output — stored as `max_rel_error` in `samples`.
3. **Tolerance-compliant case percentage** — captured from collector output — stored as `tolerance_compliance` in `samples`.
4. **Test case coverage count** — captured from collector output — stored as `coverage_count` in `samples`.
5. **Test case failure count (failure_count** — captured from collector output — stored as `test_case_failure_count_failure_count` in `samples`.


## Framework

| Component | Role |
|---|---|
| Bash | Required Framework inventory item |
| SQLite | Required Framework inventory item |
| Python | Required Framework inventory item |
| PyYAML | Required Framework inventory item |
| ROCm Runtime | Required Framework inventory item |
| PyTorch-ROCm | Required Framework inventory item |
| HIP/ROCm | Required Framework inventory item |


## Installation and Execution Summary

Run local PyTorch GPU matmul and conv2d for each yaml op_name/dtype/shape, compare each result to a CPU FP32 reference using rtol/atol, and emit error counts, to measure tensor-op numerical correctness. Does not invoke pytest or GitHub test_ops.py


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
5. All required aggregate metrics are physically sensible (positive values). Per-sample `max_abs_error`, `max_rel_error`, `tolerance_compliance`, `coverage_count`, `test_case_failure_count_failure_count` columns are finite for every row.
6. At least 2 sample rows exist for the latest `run_id` (sweep coverage).
7. No sample has `status = 'error'`.

### Baseline / Threshold configuration (`config/benchmark_config.yaml`)

```yaml
thresholds:
  max_abs_error_min: 0
  max_abs_error_max: 100
  max_rel_error_min: 0
  max_rel_error_max: 1000000000.0
  tolerance_compliance_min: 100
  tolerance_compliance_max: 100
  coverage_count_min: 1
  failure_count_max: 0
```

Threshold key suffixes encode comparison direction when `thresholds:` is present: `_min` → observed value must be ≥ threshold. `_max` → observed value must be ≤ threshold. Informational `baselines:` ranges are not pass/fail gates. Parameters in play: `device_id`, `op_name`, `dtype`, `shape`, `rtol`, `atol`, `num_iterations`, `seed`.
