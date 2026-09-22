# Gary Michael Bass

Index of GPU benchmark repositories: **32 workloads × AMD + NVIDIA × Ubuntu 24.04 + 26.04**.

Same workload number in each hundred-block is the same experiment on a different platform.

| Block | Vendor | OS | Workloads |
|------:|--------|-----|-----------|
| 100 | AMD (ROCm) | Ubuntu 24.04 | [101–132](#100--amd--ubuntu-2404-rocm) |
| 200 | NVIDIA (CUDA) | Ubuntu 24.04 | [201–232](#200--nvidia--ubuntu-2404-cuda) |
| 300 | AMD (ROCm) | Ubuntu 26.04 | [301–332](#300--amd--ubuntu-2604-rocm) |
| 400 | NVIDIA (CUDA) | Ubuntu 26.04 | [401–432](#400--nvidia--ubuntu-2604-cuda) |

| Offset | Category |
|--------|----------|
| x01–x13 | System, storage, CPU, NUMA, PMU |
| x14–x20 | GPU copy / HBM / collectives / GEMM / conv / HPL |
| x21–x26 | Training and model forward |
| x27–x32 | vLLM, SGLang, RAG |

## 100 · AMD · Ubuntu 24.04 (ROCm)

| # | Workload | Repo |
|--:|----------|------|
| 101 | System Config Verification | [sys-bench-amd-rocm-stack-validation](https://github.com/garymichaelbass/sys-bench-amd-rocm-stack-validation) |
| 102 | ROCm System Validation (clocks, temp, etc.) | [sys-bench-amd-rocm-health-validation](https://github.com/garymichaelbass/sys-bench-amd-rocm-health-validation) |
| 103 | CPU + System Stress (Baseline Health) | [sys-bench-amd-system-stress-stability](https://github.com/garymichaelbass/sys-bench-amd-system-stress-stability) |
| 104 | Silent Data Corruption (SDC) | [gpu-bench-amd-sdc-ecc-integrity](https://github.com/garymichaelbass/gpu-bench-amd-sdc-ecc-integrity) |
| 105 | PyTorch Tensor Op Correctness Suite | [gpu-bench-amd-pytorch-tensor-correctness](https://github.com/garymichaelbass/gpu-bench-amd-pytorch-tensor-correctness) |
| 106 | FIO NVMe Sweep | [sys-bench-amd-fio-nvme-sweep](https://github.com/garymichaelbass/sys-bench-amd-fio-nvme-sweep) |
| 107 | STREAM — CPU (Copy/Scale/Add/Triad) | [sys-bench-amd-stream-ddr5-bandwidth](https://github.com/garymichaelbass/sys-bench-amd-stream-ddr5-bandwidth) |
| 108 | iPerf3 TCP/UDP Sweep | [sys-bench-amd-iperf3-network-performance](https://github.com/garymichaelbass/sys-bench-amd-iperf3-network-performance) |
| 109 | multichase Pointer-Chase | [sys-bench-amd-multichase-numa-latency](https://github.com/garymichaelbass/sys-bench-amd-multichase-numa-latency) |
| 110 | NUMA Cache Latency Sweep | [sys-bench-amd-numa-cache-performance](https://github.com/garymichaelbass/sys-bench-amd-numa-cache-performance) |
| 111 | Linux perf PMU Analysis Harness | [sys-bench-amd-linux-perf-pmu](https://github.com/garymichaelbass/sys-bench-amd-linux-perf-pmu) |
| 112 | lmbench Microbench Suite | [sys-bench-amd-lmbench-microbench-suite](https://github.com/garymichaelbass/sys-bench-amd-lmbench-microbench-suite) |
| 113 | GUPS Random Memory | [sys-bench-amd-gups-random-memory](https://github.com/garymichaelbass/sys-bench-amd-gups-random-memory) |
| 114 | hipMemcpy Bandwidth (H2D, D2H, D2D) | [gpu-bench-amd-hipmemcpy-transfer-bandwidth](https://github.com/garymichaelbass/gpu-bench-amd-hipmemcpy-transfer-bandwidth) |
| 115 | BabelStream HBM Bandwidth | [gpu-bench-amd-babelstream-hbm-bandwidth](https://github.com/garymichaelbass/gpu-bench-amd-babelstream-hbm-bandwidth) |
| 116 | RCCL Bandwidth Test | [gpu-bench-amd-rccl-bandwidth-test](https://github.com/garymichaelbass/gpu-bench-amd-rccl-bandwidth-test) |
| 117 | GEMM / rocBLAS Microbenchmark | [gpu-bench-amd-gemm-rocblas-micro](https://github.com/garymichaelbass/gpu-bench-amd-gemm-rocblas-micro) |
| 118 | MIOpen Convolution Solver Microbenchmark | [gpu-bench-amd-miopen-convolution-micro](https://github.com/garymichaelbass/gpu-bench-amd-miopen-convolution-micro) |
| 119 | PyTorch Microkernel Suite | [gpu-bench-amd-torch-micro-suite](https://github.com/garymichaelbass/gpu-bench-amd-torch-micro-suite) |
| 120 | rocHPL FP64 | [gpu-bench-amd-linpack-rochpl-fp64](https://github.com/garymichaelbass/gpu-bench-amd-linpack-rochpl-fp64) |
| 121 | ResNet-50 FP16 Training Step (PyTorch) | [gpu-bench-amd-resnet50-pytorch-training](https://github.com/garymichaelbass/gpu-bench-amd-resnet50-pytorch-training) |
| 122 | ResNet-50 BF16 Inference Throughput Sweep | [gpu-bench-amd-resnet50-pytorch-inference](https://github.com/garymichaelbass/gpu-bench-amd-resnet50-pytorch-inference) |
| 123 | BERT Inference Sweep | [gpu-bench-amd-bert-base-inference](https://github.com/garymichaelbass/gpu-bench-amd-bert-base-inference) |
| 124 | Stable Diffusion XL Inference Baseline | [gpu-bench-amd-sdxl-diffusers-latency](https://github.com/garymichaelbass/gpu-bench-amd-sdxl-diffusers-latency) |
| 125 | DistilBERT NLP Training Baseline | [gpu-bench-amd-distilbert-hf-classification](https://github.com/garymichaelbass/gpu-bench-amd-distilbert-hf-classification) |
| 126 | JAX XLA Transformer Forward Pass | [gpu-bench-amd-jax-xla-forwardpass](https://github.com/garymichaelbass/gpu-bench-amd-jax-xla-forwardpass) |
| 127 | KV Cache Stress Test | [gpu-bench-amd-vllm-kvcache-stress](https://github.com/garymichaelbass/gpu-bench-amd-vllm-kvcache-stress) |
| 128 | vLLM Inference Throughput & Latency | [gpu-bench-amd-vllm-throughput-latency](https://github.com/garymichaelbass/gpu-bench-amd-vllm-throughput-latency) |
| 129 | vLLM Token-Generation Benchmark | [gpu-bench-amd-vllm-mistral-rocm](https://github.com/garymichaelbass/gpu-bench-amd-vllm-mistral-rocm) |
| 130 | SGLang Prompt-Response Benchmark | [gpu-bench-amd-sglang-prompt-response](https://github.com/garymichaelbass/gpu-bench-amd-sglang-prompt-response) |
| 131 | SGLang Serving Latency Benchmark | [gpu-bench-amd-sglang-serving-latency](https://github.com/garymichaelbass/gpu-bench-amd-sglang-serving-latency) |
| 132 | RAG Pipeline Sweep | [gpu-bench-amd-rag-faiss-end2end](https://github.com/garymichaelbass/gpu-bench-amd-rag-faiss-end2end) |

## 200 · NVIDIA · Ubuntu 24.04 (CUDA)

| # | Workload | Repo |
|--:|----------|------|
| 201 | System Config Verification | [sys-bench-nvidia-cuda-stack-validation](https://github.com/garymichaelbass/sys-bench-nvidia-cuda-stack-validation) |
| 202 | NVIDIA System Validation (clocks, temperature, etc.) | [sys-bench-nvidia-gpu-health-validation](https://github.com/garymichaelbass/sys-bench-nvidia-gpu-health-validation) |
| 203 | CPU + System Stress (Baseline Health) | [sys-bench-nvidia-system-stress-stability](https://github.com/garymichaelbass/sys-bench-nvidia-system-stress-stability) |
| 204 | Silent Data Corruption (SDC) | [gpu-bench-nvidia-sdc-ecc-integrity](https://github.com/garymichaelbass/gpu-bench-nvidia-sdc-ecc-integrity) |
| 205 | PyTorch Tensor Op Correctness Suite | [gpu-bench-nvidia-pytorch-tensor-correctness](https://github.com/garymichaelbass/gpu-bench-nvidia-pytorch-tensor-correctness) |
| 206 | FIO NVMe Sweep | [sys-bench-nvidia-fio-nvme-sweep](https://github.com/garymichaelbass/sys-bench-nvidia-fio-nvme-sweep) |
| 207 | STREAM — CPU (Copy/Scale/Add/Triad) | [sys-bench-nvidia-stream-ddr5-bandwidth](https://github.com/garymichaelbass/sys-bench-nvidia-stream-ddr5-bandwidth) |
| 208 | iPerf3 TCP/UDP Sweep | [sys-bench-nvidia-iperf3-network-performance](https://github.com/garymichaelbass/sys-bench-nvidia-iperf3-network-performance) |
| 209 | multichase Pointer-Chase | [sys-bench-nvidia-multichase-numa-latency](https://github.com/garymichaelbass/sys-bench-nvidia-multichase-numa-latency) |
| 210 | NUMA Cache Latency Sweep | [sys-bench-nvidia-numa-cache-performance](https://github.com/garymichaelbass/sys-bench-nvidia-numa-cache-performance) |
| 211 | Linux perf PMU Analysis Harness | [sys-bench-nvidia-linux-perf-pmu](https://github.com/garymichaelbass/sys-bench-nvidia-linux-perf-pmu) |
| 212 | lmbench Microbench Suite | [sys-bench-nvidia-lmbench-microbench-suite](https://github.com/garymichaelbass/sys-bench-nvidia-lmbench-microbench-suite) |
| 213 | GUPS Random Memory | [sys-bench-nvidia-gups-random-memory](https://github.com/garymichaelbass/sys-bench-nvidia-gups-random-memory) |
| 214 | CUDA Memcpy Bandwidth (H2D, D2H, D2D) | [gpu-bench-nvidia-memcpy-transfer-bandwidth](https://github.com/garymichaelbass/gpu-bench-nvidia-memcpy-transfer-bandwidth) |
| 215 | BabelStream HBM Bandwidth | [gpu-bench-nvidia-babelstream-hbm-bandwidth](https://github.com/garymichaelbass/gpu-bench-nvidia-babelstream-hbm-bandwidth) |
| 216 | NCCL Bandwidth Test | [gpu-bench-nvidia-nccl-bandwidth-test](https://github.com/garymichaelbass/gpu-bench-nvidia-nccl-bandwidth-test) |
| 217 | GEMM / cuBLAS Microbenchmark | [gpu-bench-nvidia-gemm-cublas-micro](https://github.com/garymichaelbass/gpu-bench-nvidia-gemm-cublas-micro) |
| 218 | cuDNN Convolution Microbenchmark | [gpu-bench-nvidia-cudnn-convolution-micro](https://github.com/garymichaelbass/gpu-bench-nvidia-cudnn-convolution-micro) |
| 219 | TorchBench Microkernels | [gpu-bench-nvidia-torch-micro-suite](https://github.com/garymichaelbass/gpu-bench-nvidia-torch-micro-suite) |
| 220 | NVIDIA HPL FP64 | [gpu-bench-nvidia-linpack-hpl-fp64](https://github.com/garymichaelbass/gpu-bench-nvidia-linpack-hpl-fp64) |
| 221 | ResNet-50 FP16 Training Step (PyTorch) | [gpu-bench-nvidia-resnet50-pytorch-training](https://github.com/garymichaelbass/gpu-bench-nvidia-resnet50-pytorch-training) |
| 222 | ResNet-50 BF16 Inference Throughput Sweep | [gpu-bench-nvidia-resnet50-pytorch-inference](https://github.com/garymichaelbass/gpu-bench-nvidia-resnet50-pytorch-inference) |
| 223 | BERT Inference Sweep | [gpu-bench-nvidia-bert-base-inference](https://github.com/garymichaelbass/gpu-bench-nvidia-bert-base-inference) |
| 224 | Stable Diffusion XL Inference Baseline | [gpu-bench-nvidia-sdxl-diffusers-latency](https://github.com/garymichaelbass/gpu-bench-nvidia-sdxl-diffusers-latency) |
| 225 | DistilBERT NLP Training Baseline | [gpu-bench-nvidia-distilbert-hf-classification](https://github.com/garymichaelbass/gpu-bench-nvidia-distilbert-hf-classification) |
| 226 | JAX XLA Transformer Forward Pass | [gpu-bench-nvidia-jax-xla-forwardpass](https://github.com/garymichaelbass/gpu-bench-nvidia-jax-xla-forwardpass) |
| 227 | KV Cache Stress Test | [gpu-bench-nvidia-vllm-kvcache-stress](https://github.com/garymichaelbass/gpu-bench-nvidia-vllm-kvcache-stress) |
| 228 | vLLM Inference Throughput & Latency | [gpu-bench-nvidia-vllm-throughput-latency](https://github.com/garymichaelbass/gpu-bench-nvidia-vllm-throughput-latency) |
| 229 | vLLM Token-Generation Benchmark | [gpu-bench-nvidia-vllm-mistral-cuda](https://github.com/garymichaelbass/gpu-bench-nvidia-vllm-mistral-cuda) |
| 230 | SGLang Prompt-Response Benchmark | [gpu-bench-nvidia-sglang-prompt-response](https://github.com/garymichaelbass/gpu-bench-nvidia-sglang-prompt-response) |
| 231 | SGLang Serving Latency Benchmark | [gpu-bench-nvidia-sglang-serving-latency](https://github.com/garymichaelbass/gpu-bench-nvidia-sglang-serving-latency) |
| 232 | RAG Pipeline Sweep | [gpu-bench-nvidia-rag-faiss-end2end](https://github.com/garymichaelbass/gpu-bench-nvidia-rag-faiss-end2end) |

## 300 · AMD · Ubuntu 26.04 (ROCm)

Same names as the 100-block plus `-ubu2604`.

| # | Workload | Repo |
|--:|----------|------|
| 301 | System Config Verification | [sys-bench-amd-rocm-stack-validation-ubu2604](https://github.com/garymichaelbass/sys-bench-amd-rocm-stack-validation-ubu2604) |
| 302 | ROCm System Validation | [sys-bench-amd-rocm-health-validation-ubu2604](https://github.com/garymichaelbass/sys-bench-amd-rocm-health-validation-ubu2604) |
| 303 | CPU + System Stress | [sys-bench-amd-system-stress-stability-ubu2604](https://github.com/garymichaelbass/sys-bench-amd-system-stress-stability-ubu2604) |
| 304 | Silent Data Corruption (SDC) | [gpu-bench-amd-sdc-ecc-integrity-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-sdc-ecc-integrity-ubu2604) |
| 305 | PyTorch Tensor Op Correctness | [gpu-bench-amd-pytorch-tensor-correctness-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-pytorch-tensor-correctness-ubu2604) |
| 306 | FIO NVMe Sweep | [sys-bench-amd-fio-nvme-sweep-ubu2604](https://github.com/garymichaelbass/sys-bench-amd-fio-nvme-sweep-ubu2604) |
| 307 | STREAM — CPU | [sys-bench-amd-stream-ddr5-bandwidth-ubu2604](https://github.com/garymichaelbass/sys-bench-amd-stream-ddr5-bandwidth-ubu2604) |
| 308 | iPerf3 TCP/UDP Sweep | [sys-bench-amd-iperf3-network-performance-ubu2604](https://github.com/garymichaelbass/sys-bench-amd-iperf3-network-performance-ubu2604) |
| 309 | multichase Pointer-Chase | [sys-bench-amd-multichase-numa-latency-ubu2604](https://github.com/garymichaelbass/sys-bench-amd-multichase-numa-latency-ubu2604) |
| 310 | NUMA Cache Latency Sweep | [sys-bench-amd-numa-cache-performance-ubu2604](https://github.com/garymichaelbass/sys-bench-amd-numa-cache-performance-ubu2604) |
| 311 | Linux perf PMU Analysis | [sys-bench-amd-linux-perf-pmu-ubu2604](https://github.com/garymichaelbass/sys-bench-amd-linux-perf-pmu-ubu2604) |
| 312 | lmbench Microbench Suite | [sys-bench-amd-lmbench-microbench-suite-ubu2604](https://github.com/garymichaelbass/sys-bench-amd-lmbench-microbench-suite-ubu2604) |
| 313 | GUPS Random Memory | [sys-bench-amd-gups-random-memory-ubu2604](https://github.com/garymichaelbass/sys-bench-amd-gups-random-memory-ubu2604) |
| 314 | hipMemcpy Bandwidth | [gpu-bench-amd-hipmemcpy-transfer-bandwidth-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-hipmemcpy-transfer-bandwidth-ubu2604) |
| 315 | BabelStream HBM Bandwidth | [gpu-bench-amd-babelstream-hbm-bandwidth-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-babelstream-hbm-bandwidth-ubu2604) |
| 316 | RCCL Bandwidth Test | [gpu-bench-amd-rccl-bandwidth-test-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-rccl-bandwidth-test-ubu2604) |
| 317 | GEMM / rocBLAS Microbenchmark | [gpu-bench-amd-gemm-rocblas-micro-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-gemm-rocblas-micro-ubu2604) |
| 318 | MIOpen Convolution Microbenchmark | [gpu-bench-amd-miopen-convolution-micro-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-miopen-convolution-micro-ubu2604) |
| 319 | PyTorch Microkernel Suite | [gpu-bench-amd-torch-micro-suite-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-torch-micro-suite-ubu2604) |
| 320 | rocHPL FP64 | [gpu-bench-amd-linpack-rochpl-fp64-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-linpack-rochpl-fp64-ubu2604) |
| 321 | ResNet-50 FP16 Training | [gpu-bench-amd-resnet50-pytorch-training-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-resnet50-pytorch-training-ubu2604) |
| 322 | ResNet-50 BF16 Inference | [gpu-bench-amd-resnet50-pytorch-inference-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-resnet50-pytorch-inference-ubu2604) |
| 323 | BERT Inference Sweep | [gpu-bench-amd-bert-base-inference-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-bert-base-inference-ubu2604) |
| 324 | SDXL Inference Baseline | [gpu-bench-amd-sdxl-diffusers-latency-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-sdxl-diffusers-latency-ubu2604) |
| 325 | DistilBERT Training Baseline | [gpu-bench-amd-distilbert-hf-classification-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-distilbert-hf-classification-ubu2604) |
| 326 | JAX XLA Transformer Forward | [gpu-bench-amd-jax-xla-forwardpass-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-jax-xla-forwardpass-ubu2604) |
| 327 | KV Cache Stress Test | [gpu-bench-amd-vllm-kvcache-stress-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-vllm-kvcache-stress-ubu2604) |
| 328 | vLLM Throughput & Latency | [gpu-bench-amd-vllm-throughput-latency-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-vllm-throughput-latency-ubu2604) |
| 329 | vLLM Token-Generation | [gpu-bench-amd-vllm-mistral-rocm-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-vllm-mistral-rocm-ubu2604) |
| 330 | SGLang Prompt-Response | [gpu-bench-amd-sglang-prompt-response-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-sglang-prompt-response-ubu2604) |
| 331 | SGLang Serving Latency | [gpu-bench-amd-sglang-serving-latency-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-sglang-serving-latency-ubu2604) |
| 332 | RAG Pipeline Sweep | [gpu-bench-amd-rag-faiss-end2end-ubu2604](https://github.com/garymichaelbass/gpu-bench-amd-rag-faiss-end2end-ubu2604) |

## 400 · NVIDIA · Ubuntu 26.04 (CUDA)

Same names as the 200-block plus `-ubu2604`.

| # | Workload | Repo |
|--:|----------|------|
| 401 | System Config Verification | [sys-bench-nvidia-cuda-stack-validation-ubu2604](https://github.com/garymichaelbass/sys-bench-nvidia-cuda-stack-validation-ubu2604) |
| 402 | NVIDIA System Validation | [sys-bench-nvidia-gpu-health-validation-ubu2604](https://github.com/garymichaelbass/sys-bench-nvidia-gpu-health-validation-ubu2604) |
| 403 | CPU + System Stress | [sys-bench-nvidia-system-stress-stability-ubu2604](https://github.com/garymichaelbass/sys-bench-nvidia-system-stress-stability-ubu2604) |
| 404 | Silent Data Corruption (SDC) | [gpu-bench-nvidia-sdc-ecc-integrity-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-sdc-ecc-integrity-ubu2604) |
| 405 | PyTorch Tensor Op Correctness | [gpu-bench-nvidia-pytorch-tensor-correctness-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-pytorch-tensor-correctness-ubu2604) |
| 406 | FIO NVMe Sweep | [sys-bench-nvidia-fio-nvme-sweep-ubu2604](https://github.com/garymichaelbass/sys-bench-nvidia-fio-nvme-sweep-ubu2604) |
| 407 | STREAM — CPU | [sys-bench-nvidia-stream-ddr5-bandwidth-ubu2604](https://github.com/garymichaelbass/sys-bench-nvidia-stream-ddr5-bandwidth-ubu2604) |
| 408 | iPerf3 TCP/UDP Sweep | [sys-bench-nvidia-iperf3-network-performance-ubu2604](https://github.com/garymichaelbass/sys-bench-nvidia-iperf3-network-performance-ubu2604) |
| 409 | multichase Pointer-Chase | [sys-bench-nvidia-multichase-numa-latency-ubu2604](https://github.com/garymichaelbass/sys-bench-nvidia-multichase-numa-latency-ubu2604) |
| 410 | NUMA Cache Latency Sweep | [sys-bench-nvidia-numa-cache-performance-ubu2604](https://github.com/garymichaelbass/sys-bench-nvidia-numa-cache-performance-ubu2604) |
| 411 | Linux perf PMU Analysis | [sys-bench-nvidia-linux-perf-pmu-ubu2604](https://github.com/garymichaelbass/sys-bench-nvidia-linux-perf-pmu-ubu2604) |
| 412 | lmbench Microbench Suite | [sys-bench-nvidia-lmbench-microbench-suite-ubu2604](https://github.com/garymichaelbass/sys-bench-nvidia-lmbench-microbench-suite-ubu2604) |
| 413 | GUPS Random Memory | [sys-bench-nvidia-gups-random-memory-ubu2604](https://github.com/garymichaelbass/sys-bench-nvidia-gups-random-memory-ubu2604) |
| 414 | CUDA Memcpy Bandwidth | [gpu-bench-nvidia-memcpy-transfer-bandwidth-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-memcpy-transfer-bandwidth-ubu2604) |
| 415 | BabelStream HBM Bandwidth | [gpu-bench-nvidia-babelstream-hbm-bandwidth-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-babelstream-hbm-bandwidth-ubu2604) |
| 416 | NCCL Bandwidth Test | [gpu-bench-nvidia-nccl-bandwidth-test-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-nccl-bandwidth-test-ubu2604) |
| 417 | GEMM / cuBLAS Microbenchmark | [gpu-bench-nvidia-gemm-cublas-micro-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-gemm-cublas-micro-ubu2604) |
| 418 | cuDNN Convolution Microbenchmark | [gpu-bench-nvidia-cudnn-convolution-micro-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-cudnn-convolution-micro-ubu2604) |
| 419 | TorchBench Microkernels | [gpu-bench-nvidia-torch-micro-suite-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-torch-micro-suite-ubu2604) |
| 420 | NVIDIA HPL FP64 | [gpu-bench-nvidia-linpack-hpl-fp64-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-linpack-hpl-fp64-ubu2604) |
| 421 | ResNet-50 FP16 Training | [gpu-bench-nvidia-resnet50-pytorch-training-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-resnet50-pytorch-training-ubu2604) |
| 422 | ResNet-50 BF16 Inference | [gpu-bench-nvidia-resnet50-pytorch-inference-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-resnet50-pytorch-inference-ubu2604) |
| 423 | BERT Inference Sweep | [gpu-bench-nvidia-bert-base-inference-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-bert-base-inference-ubu2604) |
| 424 | SDXL Inference Baseline | [gpu-bench-nvidia-sdxl-diffusers-latency-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-sdxl-diffusers-latency-ubu2604) |
| 425 | DistilBERT Training Baseline | [gpu-bench-nvidia-distilbert-hf-classification-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-distilbert-hf-classification-ubu2604) |
| 426 | JAX XLA Transformer Forward | [gpu-bench-nvidia-jax-xla-forwardpass-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-jax-xla-forwardpass-ubu2604) |
| 427 | KV Cache Stress Test | [gpu-bench-nvidia-vllm-kvcache-stress-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-vllm-kvcache-stress-ubu2604) |
| 428 | vLLM Throughput & Latency | [gpu-bench-nvidia-vllm-throughput-latency-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-vllm-throughput-latency-ubu2604) |
| 429 | vLLM Token-Generation | [gpu-bench-nvidia-vllm-mistral-cuda-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-vllm-mistral-cuda-ubu2604) |
| 430 | SGLang Prompt-Response | [gpu-bench-nvidia-sglang-prompt-response-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-sglang-prompt-response-ubu2604) |
| 431 | SGLang Serving Latency | [gpu-bench-nvidia-sglang-serving-latency-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-sglang-serving-latency-ubu2604) |
| 432 | RAG Pipeline Sweep | [gpu-bench-nvidia-rag-faiss-end2end-ubu2604](https://github.com/garymichaelbass/gpu-bench-nvidia-rag-faiss-end2end-ubu2604) |

Hardware SKU, stack versions, run commands, and results live in each workload repo — not in this index.