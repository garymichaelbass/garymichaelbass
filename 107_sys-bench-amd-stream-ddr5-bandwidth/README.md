# STREAM - CPU (Copy/Scale/Add/Triad Benchmark

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![CI](https://img.shields.io/badge/CI-host--safe-green.svg)](.github/workflows/ci.yml)

Target: Ubuntu 24.04 · AMD · see Hardware Requirements. This is a host benchmark, not a laptop `pip install` project.


## Quick Start

```bash
git clone https://github.com/GaryMichaelBass/sys-bench-amd-stream-ddr5-bandwidth.git
cd sys-bench-amd-stream-ddr5-bandwidth
bash setup.sh --assume-yes
bash run_benchmark.sh --profile smoke --validate
```

The smoke command runs the configured smoke test. Results are written to `results/benchmark.db` and `results/summary.json`.

This workload is local-only and does not support remote SSH execution in `setup.sh` or `run_benchmark.sh`.

### Prerequisites

This is a host benchmark, not a laptop `pip install` project. `setup.sh` needs root or sudo.

- OS: Ubuntu 24.04
- GPU/vendor from Hardware Config: Digital Ocean VM (gpu-mi300x1-192gb,20 vCPUs, 240GB RAM, 720GB NVMe), 1xMI300X(192GB-HBM, gfx942, 304CUs
- N/A - ROCm not used
- Python 3.12.3

```mermaid
flowchart LR
  setup.sh --> run_benchmark.sh --> parse_results.py --> results/benchmark.db
```


## 1. Overview

Compile official STREAM src/stream.c with gcc -O3 -fopenmp, run build/stream under OMP_NUM_THREADS, parse Copy/Scale/Add/Triad Best Rate MB/s, convert to GB/s, and compute triad/400 efficiency, to measure CPU STREAM bandwidth. numactl is not used Compiles official STREAM src/stream.c inline and runs build/stream with OMP_NUM_THREADS. num_threads: OpenMP workers. array_size: STREAM_ARRAY_SIZE. num_iterations: NTIMES. numactl is not used. output_format: csv Target hardware: Digital Ocean VM (gpu-mi300x1-192gb,20 vCPUs, 240GB RAM, 720GB NVMe), 1xMI300X(192GB-HBM, gfx942, 304CUs. Implementation components: stream-collect-amd, stream-reference, harness-self-check.


## 2. What It Validates

Validates Copy/Scale/Add/Triad Best Rate parse and triad/400 efficiency. numactl pinning is not applied

- Triad bandwidth is recorded as `triad_bandwidth_gb_s` and satisfies configured yaml gates when present.
- Copy bandwidth is recorded as `copy_bandwidth_gb_s` and satisfies configured yaml gates when present.
- Scale bandwidth is recorded as `scale_bandwidth_gb_s` and satisfies configured yaml gates when present.
- Add bandwidth is recorded as `add_bandwidth_gb_s` and satisfies configured yaml gates when present.
- Achieved DDR5 memory efficiency (achieved_ddr5_memory_efficiency is recorded as `achieved_ddr5_memory_efficiency_achieved_ddr5_memory_efficiency` and satisfies configured yaml gates when present.


## 3. Metrics Captured

1. **Triad bandwidth** — collector/parser field — `samples.triad_bandwidth_gb_s`
2. **Copy bandwidth** — collector/parser field — `samples.copy_bandwidth_gb_s`
3. **Scale bandwidth** — collector/parser field — `samples.scale_bandwidth_gb_s`
4. **Add bandwidth** — collector/parser field — `samples.add_bandwidth_gb_s`
5. **Achieved DDR5 memory efficiency (achieved_ddr5_memory_efficiency** — collector/parser field — `samples.achieved_ddr5_memory_efficiency_achieved_ddr5_memory_efficiency`


## 4. Hardware Requirements

### Supported environment

A compatible AMD GPU on Ubuntu 24.04 with the ROCm family from Framework and Python 3.12.3. Other GPUs in the same vendor/stack may work but have not been validated against the reference baseline.

- Ubuntu 24.04
- AMD GPU with N/A - ROCm not used
- Python 3.12.3

### Reference validation environment

The tables below describe the machine used to generate the reference results. They are not a requirement that every user buy that exact cloud instance.

### System

| Component | Specification |
|---|---|
| Provider | Digital Ocean |
| Droplet/instance type | gpu-mi300x1-192gb |
| vCPUs | 20 |
| RAM | 240GB |
| Storage | 720GB NVMe |

### GPU

| Component | Specification |
|---|---|
| GPU Count | 1 |
| GPU Model | MI300X |
| Architecture | gfx942 |
| Compute Units | 304 |
| HBM | 192GB |


## 5. Software Requirements

| Component | Version |
|---|---|
| OS | Ubuntu 24.04 |
| Kernel | kernel 6.8.0 |
| Python | Python 3.12.3 |
| ROCm | N/A - ROCm not used |
| rocBLAS | N/A - rocBLAS not used |
| PyYAML | see Installation and Execution Summary |
| C (not C++) | see Installation and Execution Summary |
| GCC | see Installation and Execution Summary |
| OpenMP | see Installation and Execution Summary |


## 6. Installation

```bash
git clone https://github.com/GaryMichaelBass/sys-bench-amd-stream-ddr5-bandwidth.git
cd sys-bench-amd-stream-ddr5-bandwidth
sudo bash setup.sh --assume-yes
```

> **Note:**
> - `setup.sh` installs Python venv prerequisites idempotently on fresh Ubuntu images before creating an isolated per-repository environment at the repository-local `.venv` path; do not install benchmark packages into a global Python environment.
> - `BENCHMARK_PYTHON` may select the interpreter used to create that environment (for example `/usr/bin/python3.12`); each repository may use a different interpreter and venv path, and the matching `pythonX.Y-venv` package must be installed.
> - For workload-inherent ROCm tasks, default `bash setup.sh` executes ROCm install steps 1-23 from `scripts/lib/rocm_install.sh` (runtime 1-12, repo 13-17, RVS 18-23) with explicit skip flags as advanced overrides.
> - On first local invocation, `setup.sh` prompts for confirmation that up to two reboots may occur and that setup auto-resumes after each reboot (Enter to continue). `--assume-yes` skips that prompt.
> - `setup.sh` writes a chronological install status file at `results/install_status.txt`, writes bare executed install commands to `results/install_commands.txt`, and keeps a mirrored install-status block in `/etc/motd` during reboot-driven install.
> - During reboot-driven install, `setup.sh` updates `/etc/motd` with in-progress phase/resume status and writes a persistent completion status block when installation is finished.
> - `/etc/motd` should include operator guidance lines: `To see latest status on install, execute the following:` followed by `cat /root/sys-bench-amd-stream-ddr5-bandwidth/results/install_status.txt`.
> - On successful local completion, `setup.sh` emits a `wall` broadcast (`setup.sh now complete`).


## 7. Running the Benchmark

```bash
bash run_benchmark.sh --help
bash run_benchmark.sh --profile smoke --validate
bash run_benchmark.sh --profile smoke --validate --numa-node 0 --num-threads 4 --thread-affinity core --page-size 4KB --dtype FP64 --array-size 10000000 --num-iterations 2
BENCHMARK_PYTHON=/usr/bin/python3.12 bash run_benchmark.sh --profile smoke --validate
bash run_benchmark.sh --smoke --validate
bash run_benchmark.sh --baseline --validate
bash run_benchmark.sh --extended --validate
```

`run_benchmark.sh --help` prints the `usage()` page and exits without running setup. `run_benchmark.sh` automatically invokes `scripts/ensure_setup.sh` when `.setup_state` is absent; the operator reruns the command after a reboot-driven setup resumes. A benchmark statistics summary block is printed at the end of a successful run (unless `--quiet` is used), and that summary includes extended statistics (min, max, mean, median, stddev, p95) where applicable.

| Option | Default | Description |
|---|---|---|
| --numa-node | 0 | Profile parameter `numa_node` |
| --num-threads | 4 | Profile parameter `num_threads` |
| --thread-affinity | core | Profile parameter `thread_affinity` |
| --page-size | 4KB | Profile parameter `page_size` |
| --dtype | FP64 | Profile parameter `dtype` |
| --array-size | 10000000 | Profile parameter `array_size` |
| --kernel-types | yaml | Documentary sweep/list; omit so yaml expands cases |
| --num-iterations | 2 | Profile parameter `num_iterations` |
| --config | config/benchmark_config.yaml | Sweep/threshold yaml |
| --profile | smoke | Profile name |
| --smoke | | Run smoke profile |
| --baseline | | Run baseline profile |
| --extended | | Run extended profile |
| --validate | | Run validator after parse |
| --no-validate | | Skip validator |
| --quiet | | Suppress end-of-run summary |
| --log-level | info | Log verbosity |
| --save-options-file | PATH | Write resolved options |
| --phase | phaseN or N | Resume a named phase |
| --phase1 | | Run phase 1 |
| --phase2 | | Run phase 2 |
| --phase3 | | Parse only; requires --raw-file |
| --phase4 | | Run phase 4 |
| --raw-file | | Existing raw file for phase3 |
| --matrix-definition | | Print this workload's matrix row |
| --help | | Print usage and exit |

**Validating results separately:**

```bash
export BENCHMARK_PYTHON=/usr/bin/python3.13  # optional
python3 -m venv .venv
source ".venv/bin/activate"
".venv/bin/python" scripts/validate_results.py
```


## 8. Output

### `results/benchmark.db` (SQLite)

**`runs`** — one row per `run_benchmark.sh` execution.

| Column | Meaning |
|---|---|
| run_id | Unique run identifier |
| benchmark_id | 107 |
| status | ok/error/timeout/partial |
| started_at | ISO-8601 UTC start |
| finished_at | ISO-8601 UTC stop |
| total_samples | Sweep-point counter |
| passed_samples | Passed sweep-point counter |

**`samples`** — one row per parameter combination swept.

| Column | Meaning |
|---|---|
| run_id | FK to runs |
| sample_index | Sweep index |
| status | ok/error |
| numa_node | Sweep parameter |
| num_threads | Sweep parameter |
| thread_affinity | Sweep parameter |
| page_size | Sweep parameter |
| dtype | Sweep parameter |
| array_size | Sweep parameter |
| kernel_types | Sweep parameter |
| num_iterations | Sweep parameter |
| triad_bandwidth_gb_s | Metric |
| copy_bandwidth_gb_s | Metric |
| scale_bandwidth_gb_s | Metric |
| add_bandwidth_gb_s | Metric |
| achieved_ddr5_memory_efficiency_achieved_ddr5_memory_efficiency | Metric |

### Per-run artifact directory

Each execution writes to `results/raw/YYYYMMDD_HHMMSS_<repo_name>_<hostname>/` and includes at minimum: `run.log`, `commands_executed.sh`, `env_variables.txt`, `journal_warnings.txt` (`journalctl -p warning`, run-window scoped), `script.sh`, raw benchmark dual-format exports (`raw_results.csv`, `raw_results.jsonl`), per-run sample exports in CSV and JSON, raw tool output text, and the Excel-sourced inventory files `hardware_info.txt`, `software_info.txt`, and `errors_info.txt` written into that same per-run directory by `scripts/collect_hw_sw_info.sh` from `config/hw_sw_info_commands.xlsx`. Do not write `system_info.txt`. `errors_info.txt` records unavailable probes without replacing the benchmark result status.

`/root/runtime_ledger.csv` receives one row per invocation. Column order matches `scripts/update_runtime_ledger.py`, including `total_runtime_mm_ss` as `mm:ss`, hardware/software fields, metric pairs, `run_benchmark_command_submitted`, `run_benchmark_command_fully_resolved`, `Parameter_01_Name`/`Parameter_01_Value` through `Parameter_20_Name`/`Parameter_20_Value`, `parameters_set`, and notes.

### `results/summary.json`

Consolidated metrics from the most recent run — suitable for CI artifact upload or dashboard ingestion.

### `results/raw/<timestamp>.txt`

Raw collector output consistent with STREAM stdout plus a normalized CSV aggregate.


## 9. Baselines / Thresholds

Expected ranges live in `config/benchmark_config.yaml` under `baselines:` when published. No numeric published baseline was provided for every metric.

To update baselines or thresholds, edit `config/benchmark_config.yaml` — never edit validation code directly.


## 10. Troubleshooting

**`setup.sh` reports missing ROCm tools**
- **Cause:** ROCm runtime/repository steps have not completed on this host.
- **Fix:**
```bash
sudo bash setup.sh --assume-yes
```

**Collector or parser records status=error**
- **Cause:** A required tool from Framework is missing or produced unparseable output.
- **Fix:**
```bash
bash run_benchmark.sh --profile smoke --validate
```

**Threshold or baseline validation failed**
- **Cause:** A metric is missing, non-finite, or outside `config/benchmark_config.yaml` gates.
- **Fix:**
```bash
".venv/bin/python" scripts/validate_results.py --db results/benchmark.db --config config/benchmark_config.yaml
```

**`.venv` missing or wrong interpreter**
- **Cause:** Setup has not created the repository-local environment.
- **Fix:**
```bash
export BENCHMARK_PYTHON=/usr/bin/python3.12
sudo bash setup.sh --assume-yes
```


## 11. NVIDIA H100 Coding Differences

This is an AMD ROCm workload. An NVIDIA counterpart would use CUDA/DCGM tooling rather than the ROCm probes listed in Framework.

## Repository layout

```text
.
├── setup.sh
├── run_benchmark.sh
├── benchmark_specification.json
├── config/
├── scripts/
├── src/
├── tests/
├── docs/
├── results/
└── LICENSE
```

## License

Apache License 2.0. See `LICENSE` and `legal/NOTICE`.
