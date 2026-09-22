# NVIDIA PyTorch / JAX install contract

Use this contract when `GPU Vendor` is NVIDIA and `Framework` includes PyTorch, torchvision, JAX, or Hugging Face Transformers.

Do **not** use this helper on AMD / ROCm workloads. AMD continues to follow [`rocm-pytorch-install-contract.md`](rocm-pytorch-install-contract.md).

## Rules

1. Do not list `torch`, `torchvision`, `torchaudio`, `jax`, `vllm`, or `sglang` in `requirements.txt`. Parser-only pins such as `PyYAML>=6.0` stay there.
2. Install CUDA wheels from the official PyTorch CUDA index, never unconstrained default PyPI `torch`.
3. Ubuntu 24.04 default pin: `torch==2.7.1+cu128` from `https://download.pytorch.org/whl/cu128`.
4. Ubuntu 26.04 default pin: `torch==2.13.0+cu130` from `https://download.pytorch.org/whl/cu130`. Workloads 430/431 keep their overlay pin (`torch==2.9.1+cu130`) inside `scripts/install_sglang_nvidia.sh`. Ubuntu 24.04 230/231 override the default 2.7.1+cu128 pin: `torch==2.13.0+cu130` plus `sglang==0.5.19` / `sglang-kernel==0.4.6.post1` (see [`nvidia-sglang-install-contract.md`](nvidia-sglang-install-contract.md)).
5. Install torchvision only when Framework or the implementation requires it (`BENCHMARK_INSTALL_TORCHVISION=1`).
6. Install `jax[cuda12]` only when Framework includes JAX.
7. Install `transformers` / `datasets` only when Framework includes Transformers, BERT, DistilBERT, or Hugging Face.
8. After CUDA torch, install `numpy` so Torch does not warn `Failed to initialize NumPy` (205 tensor correctness).
9. `setup.sh` must verify `torch.cuda.is_available()` (and the matching JAX/Transformers import) before writing `.setup_state`.
10. vLLM and SGLang overlay `setup.sh` files perform their own wheel install. Do not also force `install_pytorch_nvidia.sh` on those workloads.
11. Never source `scripts/lib/rocm_install.sh` and never call `scripts/install_pytorch_nvidia.sh` from `setup_rocm_reboot_skeleton.sh`.

## Helper

Generated NVIDIA repositories receive `scripts/install_pytorch_nvidia.sh` from the template `scripts/` tree. The canonical NVIDIA setup skeleton calls it when Framework requires those wheels.
