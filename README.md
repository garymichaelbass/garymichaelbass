# GPU Performance Benchmarking & Platform Validation Matrix

A standardized matrix of 32 hardware, compute, and AI inference validation workloads evaluated across AMD (ROCm) and NVIDIA (CUDA) accelerators on Ubuntu 24.04 and Ubuntu 26.04 LTS environments (128 total repositories).


## Benchmark Suites

| Suite | GPU Platform | Operating System | Workloads |
|---|---|---|---:|
| AMD / Ubuntu 24.04 | AMD / ROCm | Ubuntu 24.04 | 101–132 |
| NVIDIA / Ubuntu 24.04 | NVIDIA / CUDA | Ubuntu 24.04 | 201–232 |
| AMD / Ubuntu 26.04 | AMD / ROCm | Ubuntu 26.04 | 301–332 |
| NVIDIA / Ubuntu 26.04 | NVIDIA / CUDA | Ubuntu 26.04 | 401–432 |

**128 total benchmark workloads**

---

## Benchmark Categories

The workload suites cover five primary areas:

- **GPU Compute**
- **LLM Serving**
- **Memory / Transfer**
- **CPU / System**
- **Validation / Correctness**

---

## Benchmark Categories

The workload suites cover seven primary areas:

- **Memory, Bandwidth & Data Movement** — HBM, fabric, host/device transfers, cache, and bandwidth stress
- **AI Training & Inference** — CNN, Transformer, diffusion, and JAX model training and inference
- **Compute & Math Kernels** — BLAS, LINPACK, microbenchmarks, and mathematical compute kernels
- **LLM Inference & Serving** — vLLM throughput and latency, KV cache, token generation, and SGLang serving
- **System Validation & Reliability** — correctness testing and hardware/software health validation
- **System Profiling & Performance Analysis** — telemetry, counters, and timing characterization
- **End-to-End Application Pipelines** — full-stack application paths such as FAISS-based RAG

---

## Execution Profiles

Where applicable, workloads support three execution profiles:

| Profile | Typical Runtime | Purpose |
|---|---:|---|
| **Smoke** | ≤ 1 minute | Quick installation and functionality validation |
| **Baseline** | 3–5 minutes | Standard benchmark execution |
| **Extended** | 8-15 minutes | Longer performance characterization |

---


## How These Repositories Are Built

Every repository in this matrix is generated, not hand-written, by
[`ai-agent-gpu-benchmark-repo-generator`](https://github.com/garymichaelbass/ai-agent-gpu-benchmark-repo-generator) —
a spec-driven framework that turns one row of a workload spreadsheet into a
complete, execution-ready benchmark repo: setup script, README, PRD/SPEC,
CI workflows, parsing/validation logic, and a smoke test, with zero manual
scaffolding. See that repo for the ten-minute quickstart to generate your own.

---

## 📊 Workload Repository Matrix

| # | Workload Domain & Description | AMD (Ubuntu 24.04) | NVIDIA (Ubuntu 24.04) | AMD (Ubuntu 26.04) | NVIDIA (Ubuntu 26.04) |
| :-: | :--- | :---: | :---: | :---: | :---: |
| **01** | System Config Verification | [101](https://github.com/garymichaelbass/sys-bench-amd-rocm-stack-validation) | [201](https://github.com/garymichaelbass/sys-bench-nvidia-cuda-stack-validation) | [301](https://github.com/garymichaelbass/sys-bench-amd-rocm-stack-validation-ubu2604) | [401](https://github.com/garymichaelbass/sys-bench-nvidia-cuda-stack-validation-ubu2604) |
| **02** | System Validation (Clocks, Temp, Health) | [102](https://github.com/garymichaelbass/sys-bench-amd-rocm-health-validation) | [202](https://github.com/garymichaelbass/sys-bench-nvidia-gpu-health-validation) | [302](https://github.com/garymichaelbass/sys-bench-amd-rocm-health-validation-ubu2604) | [402](https://github.com/garymichaelbass/sys-bench-nvidia-gpu-health-validation-ubu2604) |
| **03** | CPU + System Stress Stability | [103](https://github.com/garymichaelbass/sys-bench-amd-system-stress-stability) | [203](https://github.com/garymichaelbass/sys-bench-nvidia-system-stress-stability) | [303](https://github.com/garymichaelbass/sys-bench-amd-system-stress-stability-ubu2604) | [403](https://github.com/garymichaelbass/sys-bench-nvidia-system-stress-stability-ubu2604) |
| **04** | Silent Data Corruption (SDC / ECC) | [104](https://github.com/garymichaelbass/gpu-bench-amd-sdc-ecc-integrity) | [204](https://github.com/garymichaelbass/gpu-bench-nvidia-sdc-ecc-integrity) | [304](https://github.com/garymichaelbass/gpu-bench-amd-sdc-ecc-integrity-ubu2604) | [404](https://github.com/garymichaelbass/gpu-bench-nvidia-sdc-ecc-integrity-ubu2604) |
| **05** | PyTorch Tensor Op Correctness Suite | [105](https://github.com/garymichaelbass/gpu-bench-amd-pytorch-tensor-correctness) | [205](https://github.com/garymichaelbass/gpu-bench-nvidia-pytorch-tensor-correctness) | [305](https://github.com/garymichaelbass/gpu-bench-amd-pytorch-tensor-correctness-ubu2604) | [405](https://github.com/garymichaelbass/gpu-bench-nvidia-pytorch-tensor-correctness-ubu2604) |
| **06** | FIO NVMe Storage Sweep | [106](https://github.com/garymichaelbass/sys-bench-amd-fio-nvme-sweep) | [206](https://github.com/garymichaelbass/sys-bench-nvidia-fio-nvme-sweep) | [306](https://github.com/garymichaelbass/sys-bench-amd-fio-nvme-sweep-ubu2604) | [406](https://github.com/garymichaelbass/sys-bench-nvidia-fio-nvme-sweep-ubu2604) |
| **07** | STREAM CPU DDR5 Bandwidth | [107](https://github.com/garymichaelbass/sys-bench-amd-stream-ddr5-bandwidth) | [207](https://github.com/garymichaelbass/sys-bench-nvidia-stream-ddr5-bandwidth) | [307](https://github.com/garymichaelbass/sys-bench-amd-stream-ddr5-bandwidth-ubu2604) | [407](https://github.com/garymichaelbass/sys-bench-nvidia-stream-ddr5-bandwidth-ubu2604) |
| **08** | iPerf3 Network Performance Sweep | [108](https://github.com/garymichaelbass/sys-bench-amd-iperf3-network-performance) | [208](https://github.com/garymichaelbass/sys-bench-nvidia-iperf3-network-performance) | [308](https://github.com/garymichaelbass/sys-bench-amd-iperf3-network-performance-ubu2604) | [408](https://github.com/garymichaelbass/sys-bench-nvidia-iperf3-network-performance-ubu2604) |
| **09** | multichase NUMA Latency (Pointer-Chase) | [109](https://github.com/garymichaelbass/sys-bench-amd-multichase-numa-latency) | [209](https://github.com/garymichaelbass/sys-bench-nvidia-multichase-numa-latency) | [309](https://github.com/garymichaelbass/sys-bench-amd-multichase-numa-latency-ubu2604) | [409](https://github.com/garymichaelbass/sys-bench-nvidia-multichase-numa-latency-ubu2604) |
| **10** | NUMA Cache Latency Sweep | [110](https://github.com/garymichaelbass/sys-bench-amd-numa-cache-performance) | [210](https://github.com/garymichaelbass/sys-bench-nvidia-numa-cache-performance) | [310](https://github.com/garymichaelbass/sys-bench-amd-numa-cache-performance-ubu2604) | [410](https://github.com/garymichaelbass/sys-bench-nvidia-numa-cache-performance-ubu2604) |
| **11** | Linux perf PMU Analysis Harness | [111](https://github.com/garymichaelbass/sys-bench-amd-linux-perf-pmu) | [211](https://github.com/garymichaelbass/sys-bench-nvidia-linux-perf-pmu) | [311](https://github.com/garymichaelbass/sys-bench-amd-linux-perf-pmu-ubu2604) | [411](https://github.com/garymichaelbass/sys-bench-nvidia-linux-perf-pmu-ubu2604) |
| **12** | lmbench OS Microbench Suite | [112](https://github.com/garymichaelbass/sys-bench-amd-lmbench-microbench-suite) | [212](https://github.com/garymichaelbass/sys-bench-nvidia-lmbench-microbench-suite) | [312](https://github.com/garymichaelbass/sys-bench-amd-lmbench-microbench-suite-ubu2604) | [412](https://github.com/garymichaelbass/sys-bench-nvidia-lmbench-microbench-suite-ubu2604) |
| **13** | GUPS Random Memory Access | [113](https://github.com/garymichaelbass/sys-bench-amd-gups-random-memory) | [213](https://github.com/garymichaelbass/sys-bench-nvidia-gups-random-memory) | [313](https://github.com/garymichaelbass/sys-bench-amd-gups-random-memory-ubu2604) | [413](https://github.com/garymichaelbass/sys-bench-nvidia-gups-random-memory-ubu2604) |
| **14** | Host/Device Memcpy (H2D, D2H, D2D) | [114](https://github.com/garymichaelbass/gpu-bench-amd-hipmemcpy-transfer-bandwidth) | [214](https://github.com/garymichaelbass/gpu-bench-nvidia-memcpy-transfer-bandwidth) | [314](https://github.com/garymichaelbass/gpu-bench-amd-hipmemcpy-transfer-bandwidth-ubu2604) | [414](https://github.com/garymichaelbass/gpu-bench-nvidia-memcpy-transfer-bandwidth-ubu2604) |
| **15** | BabelStream HBM Bandwidth | [115](https://github.com/garymichaelbass/gpu-bench-amd-babelstream-hbm-bandwidth) | [215](https://github.com/garymichaelbass/gpu-bench-nvidia-babelstream-hbm-bandwidth) | [315](https://github.com/garymichaelbass/gpu-bench-amd-babelstream-hbm-bandwidth-ubu2604) | [415](https://github.com/garymichaelbass/gpu-bench-nvidia-babelstream-hbm-bandwidth-ubu2604) |
| **16** | Collective Fabric Bandwidth (RCCL / NCCL) | [116](https://github.com/garymichaelbass/gpu-bench-amd-rccl-bandwidth-test) | [216](https://github.com/garymichaelbass/gpu-bench-nvidia-nccl-bandwidth-test) | [316](https://github.com/garymichaelbass/gpu-bench-amd-rccl-bandwidth-test-ubu2604) | [416](https://github.com/garymichaelbass/gpu-bench-nvidia-nccl-bandwidth-test-ubu2604) |
| **17** | GEMM Microbenchmark (rocBLAS / cuBLAS) | [117](https://github.com/garymichaelbass/gpu-bench-amd-gemm-rocblas-micro) | [217](https://github.com/garymichaelbass/gpu-bench-nvidia-gemm-cublas-micro) | [317](https://github.com/garymichaelbass/gpu-bench-amd-gemm-rocblas-micro-ubu2604) | [417](https://github.com/garymichaelbass/gpu-bench-nvidia-gemm-cublas-micro-ubu2604) |
| **18** | Convolution Solver (MIOpen / cuDNN) | [118](https://github.com/garymichaelbass/gpu-bench-amd-miopen-convolution-micro) | [218](https://github.com/garymichaelbass/gpu-bench-nvidia-cudnn-convolution-micro) | [318](https://github.com/garymichaelbass/gpu-bench-amd-miopen-convolution-micro-ubu2604) | [418](https://github.com/garymichaelbass/gpu-bench-nvidia-cudnn-convolution-micro-ubu2604) |
| **19** | PyTorch / TorchBench Microkernel Suite | [119](https://github.com/garymichaelbass/gpu-bench-amd-torch-micro-suite) | [219](https://github.com/garymichaelbass/gpu-bench-nvidia-torch-micro-suite) | [319](https://github.com/garymichaelbass/gpu-bench-amd-torch-micro-suite-ubu2604) | [419](https://github.com/garymichaelbass/gpu-bench-nvidia-torch-micro-suite-ubu2604) |
| **20** | High Performance Linpack (HPL FP64) | [120](https://github.com/garymichaelbass/gpu-bench-amd-linpack-rochpl-fp64) | [220](https://github.com/garymichaelbass/gpu-bench-nvidia-linpack-hpl-fp64) | [320](https://github.com/garymichaelbass/gpu-bench-amd-linpack-rochpl-fp64-ubu2604) | [420](https://github.com/garymichaelbass/gpu-bench-nvidia-linpack-hpl-fp64-ubu2604) |
| **21** | ResNet-50 FP16 Training Step | [121](https://github.com/garymichaelbass/gpu-bench-amd-resnet50-pytorch-training) | [221](https://github.com/garymichaelbass/gpu-bench-nvidia-resnet50-pytorch-training) | [321](https://github.com/garymichaelbass/gpu-bench-amd-resnet50-pytorch-training-ubu2604) | [421](https://github.com/garymichaelbass/gpu-bench-nvidia-resnet50-pytorch-training-ubu2604) |
| **22** | ResNet-50 BF16 Inference Throughput | [122](https://github.com/garymichaelbass/gpu-bench-amd-resnet50-pytorch-inference) | [222](https://github.com/garymichaelbass/gpu-bench-nvidia-resnet50-pytorch-inference) | [322](https://github.com/garymichaelbass/gpu-bench-amd-resnet50-pytorch-inference-ubu2604) | [422](https://github.com/garymichaelbass/gpu-bench-nvidia-resnet50-pytorch-inference-ubu2604) |
| **23** | BERT Base Inference Sweep | [123](https://github.com/garymichaelbass/gpu-bench-amd-bert-base-inference) | [223](https://github.com/garymichaelbass/gpu-bench-nvidia-bert-base-inference) | [323](https://github.com/garymichaelbass/gpu-bench-amd-bert-base-inference-ubu2604) | [423](https://github.com/garymichaelbass/gpu-bench-nvidia-bert-base-inference-ubu2604) |
| **24** | Stable Diffusion XL Latency Baseline | [124](https://github.com/garymichaelbass/gpu-bench-amd-sdxl-diffusers-latency) | [224](https://github.com/garymichaelbass/gpu-bench-nvidia-sdxl-diffusers-latency) | [324](https://github.com/garymichaelbass/gpu-bench-amd-sdxl-diffusers-latency-ubu2604) | [424](https://github.com/garymichaelbass/gpu-bench-nvidia-sdxl-diffusers-latency-ubu2604) |
| **25** | DistilBERT NLP Classification Baseline | [125](https://github.com/garymichaelbass/gpu-bench-amd-distilbert-hf-classification) | [225](https://github.com/garymichaelbass/gpu-bench-nvidia-distilbert-hf-classification) | [325](https://github.com/garymichaelbass/gpu-bench-amd-distilbert-hf-classification-ubu2604) | [425](https://github.com/garymichaelbass/gpu-bench-nvidia-distilbert-hf-classification-ubu2604) |
| **26** | JAX XLA Transformer Forward Pass | [126](https://github.com/garymichaelbass/gpu-bench-amd-jax-xla-forwardpass) | [226](https://github.com/garymichaelbass/gpu-bench-nvidia-jax-xla-forwardpass) | [326](https://github.com/garymichaelbass/gpu-bench-amd-jax-xla-forwardpass-ubu2604) | [426](https://github.com/garymichaelbass/gpu-bench-nvidia-jax-xla-forwardpass-ubu2604) |
| **27** | vLLM KV Cache Stress Test | [127](https://github.com/garymichaelbass/gpu-bench-amd-vllm-kvcache-stress) | [227](https://github.com/garymichaelbass/gpu-bench-nvidia-vllm-kvcache-stress) | [327](https://github.com/garymichaelbass/gpu-bench-amd-vllm-kvcache-stress-ubu2604) | [427](https://github.com/garymichaelbass/gpu-bench-nvidia-vllm-kvcache-stress-ubu2604) |
| **28** | vLLM Throughput & Latency Sweep | [128](https://github.com/garymichaelbass/gpu-bench-amd-vllm-throughput-latency) | [228](https://github.com/garymichaelbass/gpu-bench-nvidia-vllm-throughput-latency) | [328](https://github.com/garymichaelbass/gpu-bench-amd-vllm-throughput-latency-ubu2604) | [428](https://github.com/garymichaelbass/gpu-bench-nvidia-vllm-throughput-latency-ubu2604) |
| **29** | vLLM Mistral Token Generation | [129](https://github.com/garymichaelbass/gpu-bench-amd-vllm-mistral-rocm) | [229](https://github.com/garymichaelbass/gpu-bench-nvidia-vllm-mistral-cuda) | [329](https://github.com/garymichaelbass/gpu-bench-amd-vllm-mistral-rocm-ubu2604) | [429](https://github.com/garymichaelbass/gpu-bench-nvidia-vllm-mistral-cuda-ubu2604) |
| **30** | SGLang Prompt-Response Benchmark | [130](https://github.com/garymichaelbass/gpu-bench-amd-sglang-prompt-response) | [230](https://github.com/garymichaelbass/gpu-bench-nvidia-sglang-prompt-response) | [330](https://github.com/garymichaelbass/gpu-bench-amd-sglang-prompt-response-ubu2604) | [430](https://github.com/garymichaelbass/gpu-bench-nvidia-sglang-prompt-response-ubu2604) |
| **31** | SGLang Serving Latency Benchmark | [131](https://github.com/garymichaelbass/gpu-bench-amd-sglang-serving-latency) | [231](https://github.com/garymichaelbass/gpu-bench-nvidia-sglang-serving-latency) | [331](https://github.com/garymichaelbass/gpu-bench-amd-sglang-serving-latency-ubu2604) | [431](https://github.com/garymichaelbass/gpu-bench-nvidia-sglang-serving-latency-ubu2604) |
| **32** | End-to-End FAISS RAG Pipeline | [132](https://github.com/garymichaelbass/gpu-bench-amd-rag-faiss-end2end) | [232](https://github.com/garymichaelbass/gpu-bench-nvidia-rag-faiss-end2end) | [332](https://github.com/garymichaelbass/gpu-bench-amd-rag-faiss-end2end-ubu2604) | [432](https://github.com/garymichaelbass/gpu-bench-nvidia-rag-faiss-end2end-ubu2604) |

---

## Repository Layout & Execution Model

Every one of the 128 repositories follows the same structure, so once you've run one, you know how to run all of them:

    <repo>/
    ├── run_benchmark.sh   # entry point: bash run_benchmark.sh [--baseline|--extended]
    ├── setup.sh           # installs the ROCm/CUDA + Python stack for this workload
    ├── config/            # benchmark_config.yaml, hardware_profile.*.yaml
    ├── scripts/           # parsing/validation drivers (parse_results.py, validate_results.py, ...)
    ├── results/
    │   ├── raw/<timestamp>_<repo>_<host>/   # per-run logs, metrics, artifacts
    │   └── parsed/                          # normalized SQLite + CSV output
    └── tests/             # pytest correctness thresholds

### Running a workload

\`\`\`bash
gh repo clone garymichaelbass/<repo-name>
cd <repo-name>
bash run_benchmark.sh              # smoke profile (~1 min) — install/functionality check
bash run_benchmark.sh --baseline   # standard run (3–5 min)
bash run_benchmark.sh --extended   # full characterization (8–15 min)
\`\`\`

Each run writes latency/throughput/GFLOPS telemetry and memory high-water marks to `results/raw/`, and persists to SQLite + CSV under `results/parsed/` for cross-node aggregation.
