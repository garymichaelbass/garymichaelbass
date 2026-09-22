# SPEC.md: "The Human How"; Exact technical requirements, environment setup, implementation details, etc.


## Execution Description

Compiles official STREAM src/stream.c inline and runs build/stream with OMP_NUM_THREADS. num_threads: OpenMP workers. array_size: STREAM_ARRAY_SIZE. num_iterations: NTIMES. numactl is not used. output_format: csv Profile values are taken from `Parameters_SmokeBaselineExtend` and written to `config/benchmark_config.yaml`. Discovered implementation components: stream-collect-amd, stream-reference, harness-self-check.


## Parameters

| Parameter | CLI Flag | Tested Values | Default | Description |
|---|---|---|---|---|
| numa_node | --numa-node | 0 (smoke/baseline/extended) | 0 | Profile parameter `numa_node` from yaml |
| num_threads | --num-threads | 4 (smoke/baseline/extended) | 4 | Profile parameter `num_threads` from yaml |
| thread_affinity | --thread-affinity | core (smoke/baseline/extended) | core | Profile parameter `thread_affinity` from yaml |
| page_size | --page-size | 4KB (smoke/baseline/extended) | 4KB | Profile parameter `page_size` from yaml |
| dtype | --dtype | FP64 (smoke/baseline/extended) | FP64 | Profile parameter `dtype` from yaml |
| array_size | --array-size | 10000000 (smoke/baseline/extended) | 10000000 | Profile parameter `array_size` from yaml |
| kernel_types | --kernel-types | copy,scale,add,triad (smoke/baseline/extended) | copy,scale,add,triad | Sweep/list value. Command-column flags are documentary; omit this flag so yaml expands cases |
| num_iterations | --num-iterations | 2 (smoke/baseline/extended) | 2 | VM 2026-08-16 array_size=20M num_iterations=11000 -> 184s (3:04), 2 STREAM invocations. Extended 36000 extrapolated ~10:03, not tested. Retimed 2026-08-17 toward 3-4 min baseline; extended scaled by the same factor. 2026-08-18 retune: baseline>=3min / extended>=10min or extended~15min; NVIDIA copied from AMD. |


## Invocation

```bash
bash run_benchmark.sh --profile smoke --validate --numa-node 0 --num-threads 4 --thread-affinity core --page-size 4KB --dtype FP64 --array-size 10000000 --num-iterations 2
```


## Raw Output Format

STREAM stdout plus a normalized CSV aggregate

```text
sample_index,status,copy_bandwidth_gb_s,scale_bandwidth_gb_s,add_bandwidth_gb_s,triad_bandwidth_gb_s,achieved_ddr5_memory_efficiency,error_message
0,ok,180,175,190,185,46.25,
```


## Metrics

1. **Triad bandwidth** — captured from collector output — stored as `triad_bandwidth_gb_s` in `samples`.
2. **Copy bandwidth** — captured from collector output — stored as `copy_bandwidth_gb_s` in `samples`.
3. **Scale bandwidth** — captured from collector output — stored as `scale_bandwidth_gb_s` in `samples`.
4. **Add bandwidth** — captured from collector output — stored as `add_bandwidth_gb_s` in `samples`.
5. **Achieved DDR5 memory efficiency (achieved_ddr5_memory_efficiency** — captured from collector output — stored as `achieved_ddr5_memory_efficiency_achieved_ddr5_memory_efficiency` in `samples`.


## Framework

| Component | Role |
|---|---|
| Bash | Required Framework inventory item |
| SQLite | Required Framework inventory item |
| Python | Required Framework inventory item |
| PyYAML | Required Framework inventory item |
| C (not C++) | Required Framework inventory item |
| GCC | Required Framework inventory item |
| OpenMP | Required Framework inventory item |


## Installation and Execution Summary

Compile official STREAM src/stream.c with gcc -O3 -fopenmp, run build/stream under OMP_NUM_THREADS, parse Copy/Scale/Add/Triad Best Rate MB/s, convert to GB/s, and compute triad/400 efficiency, to measure CPU STREAM bandwidth. numactl is not used


## Platform Portability

- **AMD (primary):** gfx942, N/A - ROCm not used, Framework tools listed above.
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
5. All required aggregate metrics are physically sensible (positive values). Per-sample `triad_bandwidth_gb_s`, `copy_bandwidth_gb_s`, `scale_bandwidth_gb_s`, `add_bandwidth_gb_s`, `achieved_ddr5_memory_efficiency_achieved_ddr5_memory_efficiency` columns are finite for every row.
6. At least 2 sample rows exist for the latest `run_id` (sweep coverage).
7. No sample has `status = 'error'`.

### Baseline / Threshold configuration (`config/benchmark_config.yaml`)

```yaml
baselines: {}
  # TBD — no published reference provided
```

Threshold key suffixes encode comparison direction when `thresholds:` is present: `_min` → observed value must be ≥ threshold. `_max` → observed value must be ≤ threshold. Informational `baselines:` ranges are not pass/fail gates. Parameters in play: `numa_node`, `num_threads`, `thread_affinity`, `page_size`, `dtype`, `array_size`, `kernel_types`, `num_iterations`.
