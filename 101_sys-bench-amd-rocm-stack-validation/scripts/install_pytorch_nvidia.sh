#!/usr/bin/env bash
# File: scripts/install_pytorch_nvidia.sh
# Description: Install CUDA PyTorch/torchvision/jax/transformers from the vendor wheel index.
# Do not put torch/jax in requirements.txt. Do not call this from the ROCm setup skeleton.
# Execution: bash scripts/install_pytorch_nvidia.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"
PYTHON_BIN="${REPO_ROOT}/.venv/bin/python"
if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "[FAIL] ${PYTHON_BIN} is missing; create the venv before calling install_pytorch_nvidia.sh." >&2
  exit 1
fi

if [[ -r /etc/os-release ]]; then
  # shellcheck disable=SC1091
  . /etc/os-release
fi

BENCHMARK_INSTALL_TORCHVISION="${BENCHMARK_INSTALL_TORCHVISION:-0}"
BENCHMARK_INSTALL_JAX="${BENCHMARK_INSTALL_JAX:-0}"
BENCHMARK_INSTALL_TRANSFORMERS="${BENCHMARK_INSTALL_TRANSFORMERS:-0}"

case "${VERSION_ID:-}" in
  26.04*)
    TORCH_INDEX="${PYTORCH_CUDA_INDEX_URL:-https://download.pytorch.org/whl/cu130}"
    TORCH_SPEC="${PYTORCH_INSTALL_SPEC:-torch==2.13.0+cu130}"
    VISION_SPEC="${TORCHVISION_INSTALL_SPEC:-torchvision==0.28.0+cu130}"
    ;;
  *)
    TORCH_INDEX="${PYTORCH_CUDA_INDEX_URL:-https://download.pytorch.org/whl/cu128}"
    TORCH_SPEC="${PYTORCH_INSTALL_SPEC:-torch==2.7.1+cu128}"
    VISION_SPEC="${TORCHVISION_INSTALL_SPEC:-torchvision}"
    ;;
esac

echo "[INFO] pip install ${TORCH_SPEC} --index-url ${TORCH_INDEX}"
"${PYTHON_BIN}" -m pip install "${TORCH_SPEC}" --index-url "${TORCH_INDEX}"
echo "[INFO] pip install numpy"
"${PYTHON_BIN}" -m pip install numpy

if [[ "${BENCHMARK_INSTALL_TORCHVISION}" == "1" ]]; then
  echo "[INFO] pip install ${VISION_SPEC} --index-url ${TORCH_INDEX}"
  "${PYTHON_BIN}" -m pip install "${VISION_SPEC}" --index-url "${TORCH_INDEX}"
fi

if [[ "${BENCHMARK_INSTALL_JAX}" == "1" ]]; then
  echo "[INFO] pip install jax[cuda12]"
  "${PYTHON_BIN}" -m pip install "jax[cuda12]"
fi

if [[ "${BENCHMARK_INSTALL_TRANSFORMERS}" == "1" ]]; then
  echo "[INFO] pip install transformers datasets"
  "${PYTHON_BIN}" -m pip install transformers datasets
fi

"${PYTHON_BIN}" - <<'PY'
import os
import sys
import torch
if getattr(torch.version, "cuda", None) in {None, ""}:
    raise SystemExit("[FAIL] NVIDIA setup installed a non-CUDA torch wheel.")
if not torch.cuda.is_available():
    raise SystemExit("[FAIL] torch.cuda.is_available() is False after NVIDIA PyTorch install.")
print(f"[PASS] torch {torch.__version__} cuda={torch.version.cuda} devices={torch.cuda.device_count()}")
if os.environ.get("BENCHMARK_INSTALL_JAX") == "1":
    import jax
    print(f"[PASS] jax {jax.__version__} devices={jax.devices()}")
if os.environ.get("BENCHMARK_INSTALL_TRANSFORMERS") == "1":
    import transformers
    print(f"[PASS] transformers {transformers.__version__}")
PY
