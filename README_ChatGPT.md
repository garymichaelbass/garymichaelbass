# GPU Benchmark Workload Suites

A curated collection of **128 reproducible GPU benchmark workloads** for AMD and NVIDIA platforms across Ubuntu 24.04 and Ubuntu 26.04.

The workloads are organized into four matched 32-workload suites so that setup, execution, validation, and benchmark results can be compared consistently across GPU vendors and operating-system versions.

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

## Execution Profiles

Where applicable, workloads support three execution profiles:

| Profile | Typical Runtime | Purpose |
|---|---:|---|
| **Smoke** | ≤ 1 minute | Quick installation and functionality validation |
| **Baseline** | 3–5 minutes | Standard benchmark execution |
| **Extended** | ~20 minutes | Longer performance characterization |

---

# Benchmark Repository Index

The four sections below contain the complete benchmark repository catalog.

<details>
<summary><b>AMD / Ubuntu 24.04 — Workloads 101–132</b></summary>

<br>

| ID | Workload | Repository |
|---:|---|---|
| 101 | System Config Verification | [101_sys-bench-amd-rocm-stack-validation](https://github.com/garymichaelbass/101_sys-bench-amd-rocm-stack-validation) |
| 102 | ROCm System Validation (clocks, temp, etc.) | [102_sys-bench-amd-rocm-health-validation](https://github.com/garymichaelbass/102_sys-bench-amd-rocm-health-validation) |
| 103 | CPU + System Stress (Baseline Health) | [103_sys-bench-amd-system-stress-stability](https://github.com/garymichaelbass/103_sys-bench-amd-system-stress-stability) |
| 104 | Silent Data Corruption (SDC) | [104_gpu-bench-amd-sdc-ecc-integrity](https://github.com/garymichaelbass/104_gpu-bench-amd-sdc-ecc-integrity) |
| 105 | PyTorch Tensor Op Correctness Suite | [105_gpu-bench-amd-pytorch-tensor-correctness](https://github.com/garymichaelbass/105_gpu-bench-amd-pytorch-tensor-correctness) |
| 106 | FIO NVMe Sweep | [106_sys-bench-amd-fio-nvme-sweep](https://github.com/garymichaelbass/106_sys-bench-amd-fio-nvme-sweep) |
| 107 | STREAM - CPU (Copy/Scale/Add/Triad) | [107_sys-bench-amd-stream-ddr5-bandwidth](https://github.com/garymichaelbass/107_sys-bench-amd-stream-ddr5-bandwidth) |
| 108 | iPerf3 TCP/UDP Sweep | [108_sys-bench-amd-iperf3-network-performance](https://github.com/garymichaelbass/108_sys-bench-amd-iperf3-network-performance) |
| 109 | multichase Pointer-Chase | [109_sys-bench-amd-multichase-numa-latency](https://github.com/garymichaelbass/109_sys-bench-amd-multichase-numa-latency) |
| 110 | NUMA Cache Latency Sweep | [110_sys-bench-amd-numa-cache-performance](https://github.com/garymichaelbass/110_sys-bench-amd-numa-cache-performance) |
| 111 | Linux perf PMU Analysis Harness | [111_sys-bench-amd-linux-perf-pmu](https://github.com/garymichaelbass/111_sys-bench-amd-linux-perf-pmu) |
| 112 | lmbench Microbench Suite | [112_sys-bench-amd-lmbench-microbench-suite](https://github.com/garymichaelbass/112_sys-bench-amd-lmbench-microbench-suite) |
| 113 | GUPS Random Memory | [113_sys-bench-amd-gups-random-memory](https://github.com/garymichaelbass/113_sys-bench-amd-gups-random-memory) |
| 114 | hipMemcpy Bandwidth Test (H2D, D2H, D2D) | [114_gpu-bench-amd-hipmemcpy-transfer-bandwidth](https://github.com/garymichaelbass/114_gpu-bench-amd-hipmemcpy-transfer-bandwidth) |
| 115 | BabelStream HBM Bandwidth | [115_gpu-bench-amd-babelstream-hbm-bandwidth](https://github.com/garymichaelbass/115_gpu-bench-amd-babelstream-hbm-bandwidth) |
| 116 | RCCL Bandwidth Test | [116_gpu-bench-amd-rccl-bandwidth-test](https://github.com/garymichaelbass/116_gpu-bench-amd-rccl-bandwidth-test) |
| 117 | GEMM / rocBLAS Microbenchmark | [117_gpu-bench-amd-gemm-rocblas-micro](https://github.com/garymichaelbass/117_gpu-bench-amd-gemm-rocblas-micro) |
| 118 | MIOpen Convolution Solver Microbenchmark | [118_gpu-bench-amd-miopen-convolution-micro](https://github.com/garymichaelbass/118_gpu-bench-amd-miopen-convolution-micro) |
| 119 | PyTorch Microkernel Suite | [119_gpu-bench-amd-torch-micro-suite](https://github.com/garymichaelbass/119_gpu-bench-amd-torch-micro-suite) |
| 120 | rocHPL FP64 (High Performance Linpack) | [120_gpu-bench-amd-linpack-rochpl-fp64](https://github.com/garymichaelbass/120_gpu-bench-amd-linpack-rochpl-fp64) |
| 121 | ResNet-50 FP16 Training Step (PyTorch) | [121_gpu-bench-amd-resnet50-pytorch-training](https://github.com/garymichaelbass/121_gpu-bench-amd-resnet50-pytorch-training) |
| 122 | ResNet-50 BF16 Inference Throughput Sweep | [122_gpu-bench-amd-resnet50-pytorch-inference](https://github.com/garymichaelbass/122_gpu-bench-amd-resnet50-pytorch-inference) |
| 123 | BERT Inference Sweep | [123_gpu-bench-amd-bert-base-inference](https://github.com/garymichaelbass/123_gpu-bench-amd-bert-base-inference) |
| 124 | Stable Diffusion XL Inference Baseline | [124_gpu-bench-amd-sdxl-diffusers-latency](https://github.com/garymichaelbass/124_gpu-bench-amd-sdxl-diffusers-latency) |
| 125 | DistilBERT NLP Training Baseline | [125_gpu-bench-amd-distilbert-hf-classification](https://github.com/garymichaelbass/125_gpu-bench-amd-distilbert-hf-classification) |
| 126 | JAX XLA Transformer Forward Pass | [126_gpu-bench-amd-jax-xla-forwardpass](https://github.com/garymichaelbass/126_gpu-bench-amd-jax-xla-forwardpass) |
| 127 | KV Cache Stress Test | [127_gpu-bench-amd-vllm-kvcache-stress](https://github.com/garymichaelbass/127_gpu-bench-amd-vllm-kvcache-stress) |
| 128 | vLLM Inference Throughput & Latency | [128_gpu-bench-amd-vllm-throughput-latency](https://github.com/garymichaelbass/128_gpu-bench-amd-vllm-throughput-latency) |
| 129 | vLLM Token-Generation Benchmark | [129_gpu-bench-amd-vllm-mistral-rocm](https://github.com/garymichaelbass/129_gpu-bench-amd-vllm-mistral-rocm) |
| 130 | SGLang Prompt-Response Benchmark | [130_gpu-bench-amd-sglang-prompt-response](https://github.com/garymichaelbass/130_gpu-bench-amd-sglang-prompt-response) |
| 131 | SGLang Serving Latency Benchmark | [131_gpu-bench-amd-sglang-serving-latency](https://github.com/garymichaelbass/131_gpu-bench-amd-sglang-serving-latency) |
| 132 | RAG Pipeline Sweep | [132_gpu-bench-amd-rag-faiss-end2end](https://github.com/garymichaelbass/132_gpu-bench-amd-rag-faiss-end2end) |

</details>

---

<details>
<summary><b>NVIDIA / Ubuntu 24.04 — Workloads 201–232</b></summary>

<br>

| ID | Workload | Repository |
|---:|---|---|
| 201 | System Config Verification | [201_sys-bench-nvidia-cuda-stack-validation](https://github.com/garymichaelbass/201_sys-bench-nvidia-cuda-stack-validation) |
| 202 | NVIDIA System Validation (clocks, temperature, etc.) | [202_sys-bench-nvidia-gpu-health-validation](https://github.com/garymichaelbass/202_sys-bench-nvidia-gpu-health-validation) |
| 203 | CPU + System Stress (Baseline Health) | [203_sys-bench-nvidia-system-stress-stability](https://github.com/garymichaelbass/203_sys-bench-nvidia-system-stress-stability) |
| 204 | Silent Data Corruption (SDC) | [204_gpu-bench-nvidia-sdc-ecc-integrity](https://github.com/garymichaelbass/204_gpu-bench-nvidia-sdc-ecc-integrity) |
| 205 | PyTorch Tensor Op Correctness Suite | [205_gpu-bench-nvidia-pytorch-tensor-correctness](https://github.com/garymichaelbass/205_gpu-bench-nvidia-pytorch-tensor-correctness) |
| 206 | FIO NVMe Sweep | [206_sys-bench-nvidia-fio-nvme-sweep](https://github.com/garymichaelbass/206_sys-bench-nvidia-fio-nvme-sweep) |
| 207 | STREAM - CPU (Copy/Scale/Add/Triad) | [207_sys-bench-nvidia-stream-ddr5-bandwidth](https://github.com/garymichaelbass/207_sys-bench-nvidia-stream-ddr5-bandwidth) |
| 208 | iPerf3 TCP/UDP Sweep | [208_sys-bench-nvidia-iperf3-network-performance](https://github.com/garymichaelbass/208_sys-bench-nvidia-iperf3-network-performance) |
| 209 | multichase Pointer-Chase | [209_sys-bench-nvidia-multichase-numa-latency](https://github.com/garymichaelbass/209_sys-bench-nvidia-multichase-numa-latency) |
| 210 | NUMA Cache Latency Sweep | [210_sys-bench-nvidia-numa-cache-performance](https://github.com/garymichaelbass/210_sys-bench-nvidia-numa-cache-performance) |
| 211 | Linux perf PMU Analysis Harness | [211_sys-bench-nvidia-linux-perf-pmu](https://github.com/garymichaelbass/211_sys-bench-nvidia-linux-perf-pmu) |
| 212 | lmbench Microbench Suite | [212_sys-bench-nvidia-lmbench-microbench-suite](https://github.com/garymichaelbass/212_sys-bench-nvidia-lmbench-microbench-suite) |
| 213 | GUPS Random Memory | [213_sys-bench-nvidia-gups-random-memory](https://github.com/garymichaelbass/213_sys-bench-nvidia-gups-random-memory) |
| 214 | CUDA Memcpy Bandwidth Test (H2D, D2H, D2D) | [214_gpu-bench-nvidia-memcpy-transfer-bandwidth](https://github.com/garymichaelbass/214_gpu-bench-nvidia-memcpy-transfer-bandwidth) |
| 215 | BabelStream HBM Bandwidth | [215_gpu-bench-nvidia-babelstream-hbm-bandwidth](https://github.com/garymichaelbass/215_gpu-bench-nvidia-babelstream-hbm-bandwidth) |
| 216 | NCCL Bandwidth Test | [216_gpu-bench-nvidia-nccl-bandwidth-test](https://github.com/garymichaelbass/216_gpu-bench-nvidia-nccl-bandwidth-test) |
| 217 | GEMM / cuBLAS Microbenchmark | [217_gpu-bench-nvidia-gemm-cublas-micro](https://github.com/garymichaelbass/217_gpu-bench-nvidia-gemm-cublas-micro) |
| 218 | cuDNN Convolution Microbenchmark | [218_gpu-bench-nvidia-cudnn-convolution-micro](https://github.com/garymichaelbass/218_gpu-bench-nvidia-cudnn-convolution-micro) |
| 219 | TorchBench Microkernels | [219_gpu-bench-nvidia-torch-micro-suite](https://github.com/garymichaelbass/219_gpu-bench-nvidia-torch-micro-suite) |
| 220 | NVIDIA HPL FP64 (High Performance Linpack) | [220_gpu-bench-nvidia-linpack-hpl-fp64](https://github.com/garymichaelbass/220_gpu-bench-nvidia-linpack-hpl-fp64) |
| 221 | ResNet-50 FP16 Training Step (PyTorch) | [221_gpu-bench-nvidia-resnet50-pytorch-training](https://github.com/garymichaelbass/221_gpu-bench-nvidia-resnet50-pytorch-training) |
| 222 | ResNet-50 BF16 Inference Throughput Sweep | [222_gpu-bench-nvidia-resnet50-pytorch-inference](https://github.com/garymichaelbass/222_gpu-bench-nvidia-resnet50-pytorch-inference) |
| 223 | BERT Inference Sweep | [223_gpu-bench-nvidia-bert-base-inference](https://github.com/garymichaelbass/223_gpu-bench-nvidia-bert-base-inference) |
| 224 | Stable Diffusion XL Inference Baseline | [224_gpu-bench-nvidia-sdxl-diffusers-latency](https://github.com/garymichaelbass/224_gpu-bench-nvidia-sdxl-diffusers-latency) |
| 225 | DistilBERT NLP Training Baseline | [225_gpu-bench-nvidia-distilbert-hf-classification](https://github.com/garymichaelbass/225_gpu-bench-nvidia-distilbert-hf-classification) |
| 226 | JAX XLA Transformer Forward Pass | [226_gpu-bench-nvidia-jax-xla-forwardpass](https://github.com/garymichaelbass/226_gpu-bench-nvidia-jax-xla-forwardpass) |
| 227 | KV Cache Stress Test | [227_gpu-bench-nvidia-vllm-kvcache-stress](https://github.com/garymichaelbass/227_gpu-bench-nvidia-vllm-kvcache-stress) |
| 228 | vLLM Inference Throughput & Latency | [228_gpu-bench-nvidia-vllm-throughput-latency](https://github.com/garymichaelbass/228_gpu-bench-nvidia-vllm-throughput-latency) |
| 229 | vLLM Token-Generation Benchmark | [229_gpu-bench-nvidia-vllm-mistral-cuda](https://github.com/garymichaelbass/229_gpu-bench-nvidia-vllm-mistral-cuda) |
| 230 | SGLang Prompt-Response Benchmark | [230_gpu-bench-nvidia-sglang-prompt-response](https://github.com/garymichaelbass/230_gpu-bench-nvidia-sglang-prompt-response) |
| 231 | SGLang Serving Latency Benchmark | [231_gpu-bench-nvidia-sglang-serving-latency](https://github.com/garymichaelbass/231_gpu-bench-nvidia-sglang-serving-latency) |
| 232 | RAG Pipeline Sweep | [232_gpu-bench-nvidia-rag-faiss-end2end](https://github.com/garymichaelbass/232_gpu-bench-nvidia-rag-faiss-end2end) |

</details>

---

<details>
<summary><b>AMD / Ubuntu 26.04 — Workloads 301–332</b></summary>

<br>

| ID | Workload | Repository |
|---:|---|---|
| 301 | System Config Verification | [301_sys-bench-amd-rocm-stack-validation-ubu2604](https://github.com/garymichaelbass/301_sys-bench-amd-rocm-stack-validation-ubu2604) |
| 302 | ROCm System Validation (clocks, temp, etc.) | [302_sys-bench-amd-rocm-health-validation-ubu2604](https://github.com/garymichaelbass/302_sys-bench-amd-rocm-health-validation-ubu2604) |
| 303 | CPU + System Stress (Baseline Health) | [303_sys-bench-amd-system-stress-stability-ubu2604](https://github.com/garymichaelbass/303_sys-bench-amd-system-stress-stability-ubu2604) |
| 304 | Silent Data Corruption (SDC) | [304_gpu-bench-amd-sdc-ecc-integrity-ubu2604](https://github.com/garymichaelbass/304_gpu-bench-amd-sdc-ecc-integrity-ubu2604) |
| 305 | PyTorch Tensor Op Correctness Suite | [305_gpu-bench-amd-pytorch-tensor-correctness-ubu2604](https://github.com/garymichaelbass/305_gpu-bench-amd-pytorch-tensor-correctness-ubu2604) |
| 306 | FIO NVMe Sweep | [306_sys-bench-amd-fio-nvme-sweep-ubu2604](https://github.com/garymichaelbass/306_sys-bench-amd-fio-nvme-sweep-ubu2604) |
| 307 | STREAM - CPU (Copy/Scale/Add/Triad) | [307_sys-bench-amd-stream-ddr5-bandwidth-ubu2604](https://github.com/garymichaelbass/307_sys-bench-amd-stream-ddr5-bandwidth-ubu2604) |
| 308 | iPerf3 TCP/UDP Sweep | [308_sys-bench-amd-iperf3-network-performance-ubu2604](https://github.com/garymichaelbass/308_sys-bench-amd-iperf3-network-performance-ubu2604) |
| 309 | multichase Pointer-Chase | [309_sys-bench-amd-multichase-numa-latency-ubu2604](https://github.com/garymichaelbass/309_sys-bench-amd-multichase-numa-latency-ubu2604) |
| 310 | NUMA Cache Latency Sweep | [310_sys-bench-amd-numa-cache-performance-ubu2604](https://github.com/garymichaelbass/310_sys-bench-amd-numa-cache-performance-ubu2604) |
| 311 | Linux perf PMU Analysis Harness | [311_sys-bench-amd-linux-perf-pmu-ubu2604](https://github.com/garymichaelbass/311_sys-bench-amd-linux-perf-pmu-ubu2604) |
| 312 | lmbench Microbench Suite | [312_sys-bench-amd-lmbench-microbench-suite-ubu2604](https://github.com/garymichaelbass/312_sys-bench-amd-lmbench-microbench-suite-ubu2604) |
| 313 | GUPS Random Memory | [313_sys-bench-amd-gups-random-memory-ubu2604](https://github.com/garymichaelbass/313_sys-bench-amd-gups-random-memory-ubu2604) |
| 314 | hipMemcpy Bandwidth Test (H2D, D2H, D2D) | [314_gpu-bench-amd-hipmemcpy-transfer-bandwidth-ubu2604](https://github.com/garymichaelbass/314_gpu-bench-amd-hipmemcpy-transfer-bandwidth-ubu2604) |
| 315 | BabelStream HBM Bandwidth | [315_gpu-bench-amd-babelstream-hbm-bandwidth-ubu2604](https://github.com/garymichaelbass/315_gpu-bench-amd-babelstream-hbm-bandwidth-ubu2604) |
| 316 | RCCL Bandwidth Test | [316_gpu-bench-amd-rccl-bandwidth-test-ubu2604](https://github.com/garymichaelbass/316_gpu-bench-amd-rccl-bandwidth-test-ubu2604) |
| 317 | GEMM / rocBLAS Microbenchmark | [317_gpu-bench-amd-gemm-rocblas-micro-ubu2604](https://github.com/garymichaelbass/317_gpu-bench-amd-gemm-rocblas-micro-ubu2604) |
| 318 | MIOpen Convolution Solver Microbenchmark | [318_gpu-bench-amd-miopen-convolution-micro-ubu2604](https://github.com/garymichaelbass/318_gpu-bench-amd-miopen-convolution-micro-ubu2604) |
| 319 | PyTorch Microkernel Suite | [319_gpu-bench-amd-torch-micro-suite-ubu2604](https://github.com/garymichaelbass/319_gpu-bench-amd-torch-micro-suite-ubu2604) |
| 320 | rocHPL FP64 (High Performance Linpack) | [320_gpu-bench-amd-linpack-rochpl-fp64-ubu2604](https://github.com/garymichaelbass/320_gpu-bench-amd-linpack-rochpl-fp64-ubu2604) |
| 321 | ResNet-50 FP16 Training Step (PyTorch) | [321_gpu-bench-amd-resnet50-pytorch-training-ubu2604](https://github.com/garymichaelbass/321_gpu-bench-amd-resnet50-pytorch-training-ubu2604) |
| 322 | ResNet-50 BF16 Inference Throughput Sweep | [322_gpu-bench-amd-resnet50-pytorch-inference-ubu2604](https://github.com/garymichaelbass/322_gpu-bench-amd-resnet50-pytorch-inference-ubu2604) |
| 323 | BERT Inference Sweep | [323_gpu-bench-amd-bert-base-inference-ubu2604](https://github.com/garymichaelbass/323_gpu-bench-amd-bert-base-inference-ubu2604) |
| 324 | Stable Diffusion XL Inference Baseline | [324_gpu-bench-amd-sdxl-diffusers-latency-ubu2604](https://github.com/garymichaelbass/324_gpu-bench-amd-sdxl-diffusers-latency-ubu2604) |
| 325 | DistilBERT NLP Training Baseline | [325_gpu-bench-amd-distilbert-hf-classification-ubu2604](https://github.com/garymichaelbass/325_gpu-bench-amd-distilbert-hf-classification-ubu2604) |
| 326 | JAX XLA Transformer Forward Pass | [326_gpu-bench-amd-jax-xla-forwardpass-ubu2604](https://github.com/garymichaelbass/326_gpu-bench-amd-jax-xla-forwardpass-ubu2604) |
| 327 | KV Cache Stress Test | [327_gpu-bench-amd-vllm-kvcache-stress-ubu2604](https://github.com/garymichaelbass/327_gpu-bench-amd-vllm-kvcache-stress-ubu2604) |
| 328 | vLLM Inference Throughput & Latency | [328_gpu-bench-amd-vllm-throughput-latency-ubu2604](https://github.com/garymichaelbass/328_gpu-bench-amd-vllm-throughput-latency-ubu2604) |
| 329 | vLLM Token-Generation Benchmark | [329_gpu-bench-amd-vllm-mistral-rocm-ubu2604](https://github.com/garymichaelbass/329_gpu-bench-amd-vllm-mistral-rocm-ubu2604) |
| 330 | SGLang Prompt-Response Benchmark | [330_gpu-bench-amd-sglang-prompt-response-ubu2604](https://github.com/garymichaelbass/330_gpu-bench-amd-sglang-prompt-response-ubu2604) |
| 331 | SGLang Serving Latency Benchmark | [331_gpu-bench-amd-sglang-serving-latency-ubu2604](https://github.com/garymichaelbass/331_gpu-bench-amd-sglang-serving-latency-ubu2604) |
| 332 | RAG Pipeline Sweep | [332_gpu-bench-amd-rag-faiss-end2end-ubu2604](https://github.com/garymichaelbass/332_gpu-bench-amd-rag-faiss-end2end-ubu2604) |

</details>

---

<details>
<summary><b>NVIDIA / Ubuntu 26.04 — Workloads 401–432</b></summary>

<br>

| ID | Workload | Repository |
|---:|---|---|
| 401 | System Config Verification | [401_sys-bench-nvidia-cuda-stack-validation-ubu2604](https://github.com/garymichaelbass/401_sys-bench-nvidia-cuda-stack-validation-ubu2604) |
| 402 | NVIDIA System Validation (clocks, temperature, etc.) | [402_sys-bench-nvidia-gpu-health-validation-ubu2604](https://github.com/garymichaelbass/402_sys-bench-nvidia-gpu-health-validation-ubu2604) |
| 403 | CPU + System Stress (Baseline Health) | [403_sys-bench-nvidia-system-stress-stability-ubu2604](https://github.com/garymichaelbass/403_sys-bench-nvidia-system-stress-stability-ubu2604) |
| 404 | Silent Data Corruption (SDC) | [404_gpu-bench-nvidia-sdc-ecc-integrity-ubu2604](https://github.com/garymichaelbass/404_gpu-bench-nvidia-sdc-ecc-integrity-ubu2604) |
| 405 | PyTorch Tensor Op Correctness Suite | [405_gpu-bench-nvidia-pytorch-tensor-correctness-ubu2604](https://github.com/garymichaelbass/405_gpu-bench-nvidia-pytorch-tensor-correctness-ubu2604) |
| 406 | FIO NVMe Sweep | [406_sys-bench-nvidia-fio-nvme-sweep-ubu2604](https://github.com/garymichaelbass/406_sys-bench-nvidia-fio-nvme-sweep-ubu2604) |
| 407 | STREAM - CPU (Copy/Scale/Add/Triad) | [407_sys-bench-nvidia-stream-ddr5-bandwidth-ubu2604](https://github.com/garymichaelbass/407_sys-bench-nvidia-stream-ddr5-bandwidth-ubu2604) |
| 408 | iPerf3 TCP/UDP Sweep | [408_sys-bench-nvidia-iperf3-network-performance-ubu2604](https://github.com/garymichaelbass/408_sys-bench-nvidia-iperf3-network-performance-ubu2604) |
| 409 | multichase Pointer-Chase | [409_sys-bench-nvidia-multichase-numa-latency-ubu2604](https://github.com/garymichaelbass/409_sys-bench-nvidia-multichase-numa-latency-ubu2604) |
| 410 | NUMA Cache Latency Sweep | [410_sys-bench-nvidia-numa-cache-performance-ubu2604](https://github.com/garymichaelbass/410_sys-bench-nvidia-numa-cache-performance-ubu2604) |
| 411 | Linux perf PMU Analysis Harness | [411_sys-bench-nvidia-linux-perf-pmu-ubu2604](https://github.com/garymichaelbass/411_sys-bench-nvidia-linux-perf-pmu-ubu2604) |
| 412 | lmbench Microbench Suite | [412_sys-bench-nvidia-lmbench-microbench-suite-ubu2604](https://github.com/garymichaelbass/412_sys-bench-nvidia-lmbench-microbench-suite-ubu2604) |
| 413 | GUPS Random Memory | [413_sys-bench-nvidia-gups-random-memory-ubu2604](https://github.com/garymichaelbass/413_sys-bench-nvidia-gups-random-memory-ubu2604) |
| 414 | CUDA Memcpy Bandwidth Test (H2D, D2H, D2D) | [414_gpu-bench-nvidia-memcpy-transfer-bandwidth-ubu2604](https://github.com/garymichaelbass/414_gpu-bench-nvidia-memcpy-transfer-bandwidth-ubu2604) |
| 415 | BabelStream HBM Bandwidth | [415_gpu-bench-nvidia-babelstream-hbm-bandwidth-ubu2604](https://github.com/garymichaelbass/415_gpu-bench-nvidia-babelstream-hbm-bandwidth-ubu2604) |
| 416 | NCCL Bandwidth Test | [416_gpu-bench-nvidia-nccl-bandwidth-test-ubu2604](https://github.com/garymichaelbass/416_gpu-bench-nvidia-nccl-bandwidth-test-ubu2604) |
| 417 | GEMM / cuBLAS Microbenchmark | [417_gpu-bench-nvidia-gemm-cublas-micro-ubu2604](https://github.com/garymichaelbass/417_gpu-bench-nvidia-gemm-cublas-micro-ubu2604) |
| 418 | cuDNN Convolution Microbenchmark | [418_gpu-bench-nvidia-cudnn-convolution-micro-ubu2604](https://github.com/garymichaelbass/418_gpu-bench-nvidia-cudnn-convolution-micro-ubu2604) |
| 419 | TorchBench Microkernels | [419_gpu-bench-nvidia-torch-micro-suite-ubu2604](https://github.com/garymichaelbass/419_gpu-bench-nvidia-torch-micro-suite-ubu2604) |
| 420 | NVIDIA HPL FP64 (High Performance Linpack) | [420_gpu-bench-nvidia-linpack-hpl-fp64-ubu2604](https://github.com/garymichaelbass/420_gpu-bench-nvidia-linpack-hpl-fp64-ubu2604) |
| 421 | ResNet-50 FP16 Training Step (PyTorch) | [421_gpu-bench-nvidia-resnet50-pytorch-training-ubu2604](https://github.com/garymichaelbass/421_gpu-bench-nvidia-resnet50-pytorch-training-ubu2604) |
| 422 | ResNet-50 BF16 Inference Throughput Sweep | [422_gpu-bench-nvidia-resnet50-pytorch-inference-ubu2604](https://github.com/garymichaelbass/422_gpu-bench-nvidia-resnet50-pytorch-inference-ubu2604) |
| 423 | BERT Inference Sweep | [423_gpu-bench-nvidia-bert-base-inference-ubu2604](https://github.com/garymichaelbass/423_gpu-bench-nvidia-bert-base-inference-ubu2604) |
| 424 | Stable Diffusion XL Inference Baseline | [424_gpu-bench-nvidia-sdxl-diffusers-latency-ubu2604](https://github.com/garymichaelbass/424_gpu-bench-nvidia-sdxl-diffusers-latency-ubu2604) |
| 425 | DistilBERT NLP Training Baseline | [425_gpu-bench-nvidia-distilbert-hf-classification-ubu2604](https://github.com/garymichaelbass/425_gpu-bench-nvidia-distilbert-hf-classification-ubu2604) |
| 426 | JAX XLA Transformer Forward Pass | [426_gpu-bench-nvidia-jax-xla-forwardpass-ubu2604](https://github.com/garymichaelbass/426_gpu-bench-nvidia-jax-xla-forwardpass-ubu2604) |
| 427 | KV Cache Stress Test | [427_gpu-bench-nvidia-vllm-kvcache-stress-ubu2604](https://github.com/garymichaelbass/427_gpu-bench-nvidia-vllm-kvcache-stress-ubu2604) |
| 428 | vLLM Inference Throughput & Latency | [428_gpu-bench-nvidia-vllm-throughput-latency-ubu2604](https://github.com/garymichaelbass/428_gpu-bench-nvidia-vllm-throughput-latency-ubu2604) |
| 429 | vLLM Token-Generation Benchmark | [429_gpu-bench-nvidia-vllm-mistral-cuda-ubu2604](https://github.com/garymichaelbass/429_gpu-bench-nvidia-vllm-mistral-cuda-ubu2604) |
| 430 | SGLang Prompt-Response Benchmark | [430_gpu-bench-nvidia-sglang-prompt-response-ubu2604](https://github.com/garymichaelbass/430_gpu-bench-nvidia-sglang-prompt-response-ubu2604) |
| 431 | SGLang Serving Latency Benchmark | [431_gpu-bench-nvidia-sglang-serving-latency-ubu2604](https://github.com/garymichaelbass/431_gpu-bench-nvidia-sglang-serving-latency-ubu2604) |
| 432 | RAG Pipeline Sweep | [432_gpu-bench-nvidia-rag-faiss-end2end-ubu2604](https://github.com/garymichaelbass/432_gpu-bench-nvidia-rag-faiss-end2end-ubu2604) |

</details>

---

## Repository Structure

Each benchmark repository follows a consistent structure intended to make setup and execution repeatable.

Typical repository contents include:

```text
setup.sh
run_benchmark.sh
README.md