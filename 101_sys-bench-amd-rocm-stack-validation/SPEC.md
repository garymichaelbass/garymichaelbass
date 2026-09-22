# SPEC.md: "The Human How"; Exact technical requirements, environment setup, implementation details, etc.


## Execution Description

This workload runs seven ROCm stack probes and emits one CSV row per tool. The collector invokes `rvs --version`, `rocminfo`, `rocm-smi`, `amd-smi static`, `uname -a`, `modinfo amdgpu`, and `hipcc --version`, then compares package presence, kernel/driver substrings, and `/dev/kfd` plus `/dev/dri/renderD128` permissions to yaml expectations. Profile parameters are held fixed across smoke, baseline, and extended: there is no duration knob, and `required_packages` is a sweep/list value expanded from yaml rather than a CLI sweep-list flag. Exact `rocm_version` string compare is not performed; DCGM is not invoked.


## Parameters

| Parameter | CLI Flag | Tested Values | Default | Description |
|---|---|---|---|---|
| kernel_version | --kernel-version | 6.8.0 (smoke/baseline/extended) | 6.8.0 | Expected `uname -r` prefix compared to the live kernel |
| driver_version | --driver-version | 6 (smoke/baseline/extended) | 6 | Substring compared to amdgpu/modinfo output |
| rocm_version | --rocm-version | 7.2.1 (smoke/baseline/extended) | 7.2.1 | Documented ROCm expectation; collector checks package presence rather than an exact version string |
| required_packages | --required-packages | rocm-core,rocm-smi (smoke/baseline/extended) | rocm-core,rocm-smi | Sweep/list value. Command-column flags are documentary; omit this flag so yaml expands cases |
| permissions_check | --permissions-check | true (smoke/baseline/extended) | true | Require readable `/dev/kfd` and `/dev/dri/renderD128` |
| output_format | --output-format | csv (smoke/baseline/extended) | csv | Collector CSV format for one row per tool probe |


## Invocation

```bash
bash run_benchmark.sh --profile smoke --validate --kernel-version 6.8.0 --driver-version 6 --rocm-version 7.2.1 --permissions-check true --output-format csv
```

Omit `--required-packages` so `config/benchmark_config.yaml` expands the package list. Do not map list intent to `rvs -l`; use `rvs --version` or `rvs -g`.


## Raw Output Format

The collector writes CSV with one row per tool check plus per-tool transcripts (`rvs.txt`, `rocminfo.txt`, `rocm-smi.txt`, and the remaining probe transcripts). Authoritative header names:

```text
sample_index,check_name,rocm_package_mismatch_count,kernel_driver_mismatch_count,firmware_compliance_percent,driver_compliance_percent,permission_error_count
0,rocminfo,0,0,100,100,0
```

Units: mismatch and permission counts are integers (emitted as floats in CSV); firmware and driver compliance are percents in `[0, 100]`. Parser column names match this header. Seven tool probes are always run; profile flags do not change which tools run.


## Metrics

1. **ROCm package mismatch count** — count of missing required packages plus failed ROCm tool probes — stored as `rocm_package_mismatch_count` in `samples`.
2. **Kernel/driver mismatch count** — kernel prefix or amdgpu driver substring mismatch count — stored as `kernel_driver_mismatch_count` in `samples`.
3. **Firmware compliance percent** — firmware presence/compliance percent for the probe row — stored as `firmware_compliance_percent` in `samples`.
4. **Driver compliance percent** — driver substring compliance percent for the probe row — stored as `driver_compliance_percent` in `samples`.
5. **Permission error count** — unreadable or missing `/dev/kfd` and `/dev/dri/renderD128` count — stored as `permission_error_count` in `samples`.


## Framework

| Component | Role |
|---|---|
| Bash | Setup and run-harness orchestration |
| SQLite | Durable `results/benchmark.db` store |
| Python | Collector, parser, and validator |
| PyYAML | Load `config/benchmark_config.yaml` sweep and thresholds |
| ROCm | GPU runtime stack under test |
| rocminfo | Agent/device probe |
| rocm-smi | Device/SMI probe |
| amd-smi | Static SMI probe |
| HIP/hipcc | Compiler/version probe |
| RVS | `rvs --version` only; no GST/IET modules |


## Installation and Execution Summary

Run rvs --version, rocminfo, rocm-smi, amd-smi static, uname -a, modinfo amdgpu, hipcc --version, and dpkg-query, then compare package presence, kernel/driver substrings, and /dev/kfd plus /dev/dri/renderD128 permissions to yaml expectations, to measure ROCm stack compliance


## Platform Portability

- **AMD (primary):** gfx942 (AMD MI300X), ROCm 7.2.1, RVS/`rocminfo`/`rocm-smi`/`amd-smi`/`hipcc` stack validation. AMD-only; DCGM is not invoked.
- **NVIDIA:** This workload is AMD ROCm stack validation. NVIDIA DCGM is not invoked. An NVIDIA counterpart would probe NVIDIA stack tools rather than rocminfo/rocm-smi/amd-smi/RVS.


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

Each execution writes `results/raw/YYYYMMDD_HHMMSS_<repo_name>_<hostname>/`. Required artifacts: `run.log` (full transcript with ANSI stripped in file), `commands_executed.sh` (replayable command log), masked `env_variables.txt`, `journal_warnings.txt` (`journalctl -p warning`, run-window scoped), `script.sh` (executed harness copy), raw output text, dual raw exports (`raw_results.csv`, `raw_results.jsonl`), per-run samples CSV/JSON exports, and Excel-sourced `hardware_info.txt`, `software_info.txt`, and `errors_info.txt` in that same per-run directory. Do not write `system_info.txt`.

`run_benchmark.sh` supports resumable phase execution. Accepted forms are `--phase phase3`, `--phase 3`, and `--phase3` (same for phases 1, 2, and 4). `--raw-file <path>` points at an existing raw file for parse-only `--phase3` recovery; it is not an output-log path. `bash run_benchmark.sh --help` prints the `usage()` page and exits before setup. `bash run_benchmark.sh --matrix-definition` prints this workload's `benchmark_specification.json` field/value table and exits before setup.

### Required integrity checks (built into `validate_results.py`)

1. Latest run exists and `runs.status = 'ok'`.
2. `run.error_message` is NULL.
3. `started_at` and `finished_at` are valid ISO-8601 UTC strings.
4. All required aggregate metrics in `runs` are non-NULL and finite.
5. All required aggregate metrics are physically sensible (positive values). Per-sample `firmware_compliance_percent` and `driver_compliance_percent` are finite and in `[0, 100]`; mismatch and permission counts are finite and non-negative for every row.
6. At least 2 sample rows exist for the latest `run_id` (sweep coverage).
7. No sample has `status = 'error'`.

### Baseline / Threshold configuration (`config/benchmark_config.yaml`)

```yaml
thresholds:
  rocm_package_mismatch_count_min: 0      # compliance gate: no missing required packages
  rocm_package_mismatch_count_max: 0      # compliance gate: no missing required packages
  kernel_driver_mismatch_count_min: 0     # kernel/driver substring must match yaml
  kernel_driver_mismatch_count_max: 0     # kernel/driver substring must match yaml
  firmware_compliance_percent_min: 100    # firmware present / compliant
  firmware_compliance_percent_max: 100    # firmware present / compliant
  driver_compliance_percent_min: 100      # driver substring compliant
  driver_compliance_percent_max: 100      # driver substring compliant
  permission_error_count_min: 0           # /dev/kfd and renderD128 readable
  permission_error_count_max: 0           # /dev/kfd and renderD128 readable
```

Threshold key suffixes encode comparison direction when `thresholds:` is present: `_min` → observed value must be ≥ threshold. `_max` → observed value must be ≤ threshold. Informational `baselines:` ranges are not pass/fail gates.
