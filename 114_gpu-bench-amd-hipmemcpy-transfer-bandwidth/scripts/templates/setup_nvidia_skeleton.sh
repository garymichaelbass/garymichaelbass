#!/usr/bin/env bash
# File: scripts/templates/setup_nvidia_skeleton.sh
# Description: Canonical NVIDIA setup.sh. Installs CUDA host tools, parser deps,
# Framework-driven CUDA wheels, overlay helpers, then scripts/build.sh.
# Do not source scripts/lib/rocm_install.sh. Overlay setup.sh for vLLM/SGLang
# may replace this file; do not recopy this skeleton after overlays.
set -euo pipefail

if [[ -z "${HOME:-}" ]]; then
  HOME="$(getent passwd "$(id -u)" | cut -d: -f6 2>/dev/null || true)"
  HOME="${HOME:-/root}"
  export HOME
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_NAME="$(basename "${REPO_ROOT}")"
cd "${REPO_ROOT}"
export PATH="/usr/local/cuda/bin:/usr/local/cuda-13.3/bin:/usr/local/cuda-12.8/bin:/usr/local/cuda-12.6/bin:${PATH}"
export CUDA_HOME="${CUDA_HOME:-/usr/local/cuda}"
export LD_LIBRARY_PATH="${CUDA_HOME}/lib64:${CUDA_HOME}/targets/x86_64-linux/lib:${LD_LIBRARY_PATH:-}"

ASSUME_YES=0
usage() {
  cat <<'USAGE'
Usage: bash setup.sh [OPTIONS]

Install and verify NVIDIA host prerequisites.

  --assume-yes    Run noninteractively
  --help          Show this help and exit
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --assume-yes|-y) ASSUME_YES=1; shift ;;
    --help|-h) usage; exit 0 ;;
    --skip-rocm|--skip-rvs|--resume-auto|--no-resume-auto|--resume-from-service) shift ;;
    *) echo "[ERROR] Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

mkdir -p results src scripts bin
STATUS_FILE="${REPO_ROOT}/results/install_status.txt"
COMMANDS_FILE="${REPO_ROOT}/results/install_commands.txt"
: >> "${STATUS_FILE}"
: >> "${COMMANDS_FILE}"

log_status() { printf '%s  %s\n' "$(date -u +'%Y-%m-%d %H:%M:%S')" "$1" | tee -a "${STATUS_FILE}"; }
record_cmd() { printf '%s\n' "$1" >> "${COMMANDS_FILE}"; }

apt_install() {
  local pkg
  for pkg in "$@"; do
    if dpkg -s "${pkg}" >/dev/null 2>&1; then
      log_status "STEP|SETUP already present: ${pkg}"
      continue
    fi
    log_status "STEP|SETUP apt-get install ${pkg}"
    record_cmd "DEBIAN_FRONTEND=noninteractive apt-get install -y ${pkg}"
    DEBIAN_FRONTEND=noninteractive apt-get install -y "${pkg}" || true
  done
}

verify_cmd() {
  local name="$1"
  shift
  if ! "$@"; then
    echo "[FAIL] Required framework item failed verification: ${name}" >&2
    exit 1
  fi
  log_status "PASS|SETUP verified ${name}"
}

BENCHMARK_INSTALL_PYTORCH="${BENCHMARK_INSTALL_PYTORCH:-0}"
BENCHMARK_INSTALL_TORCHVISION="${BENCHMARK_INSTALL_TORCHVISION:-0}"
BENCHMARK_INSTALL_JAX="${BENCHMARK_INSTALL_JAX:-0}"
BENCHMARK_INSTALL_TRANSFORMERS="${BENCHMARK_INSTALL_TRANSFORMERS:-0}"

if [[ -f benchmark_specification.json ]]; then
  workload_framework="$("${BENCHMARK_PYTHON:-python3}" - <<'PY'
import json
from pathlib import Path
fields = {
    item.get("field_name", ""): str(item.get("value", ""))
    for item in json.loads(Path("benchmark_specification.json").read_text(encoding="utf-8"))
}
print(fields.get("Framework", ""))
PY
  )"
  if grep -Eiq '(^|[,[:space:]])pytorch([,-]|[[:space:]]|$)|torch' <<< "${workload_framework}" &&
     ! grep -Eiq '(^|[,[:space:]])vllm([,[:space:]]|$)|sglang' <<< "${workload_framework}"; then
    BENCHMARK_INSTALL_PYTORCH=1
  fi
  if grep -Eiq 'torchvision|resnet' <<< "${workload_framework}"; then
    BENCHMARK_INSTALL_TORCHVISION=1
    BENCHMARK_INSTALL_PYTORCH=1
  fi
  if grep -Eiq '(^|[,[:space:]])jax([,[:space:]]|$)' <<< "${workload_framework}"; then
    BENCHMARK_INSTALL_JAX=1
  fi
  if grep -Eiq 'transformers|huggingface|bert|distilbert' <<< "${workload_framework}"; then
    BENCHMARK_INSTALL_TRANSFORMERS=1
    BENCHMARK_INSTALL_PYTORCH=1
  fi
fi
export BENCHMARK_INSTALL_PYTORCH BENCHMARK_INSTALL_TORCHVISION BENCHMARK_INSTALL_JAX BENCHMARK_INSTALL_TRANSFORMERS

if [[ "${ASSUME_YES}" -ne 1 ]]; then
  echo "setup.sh will install Ubuntu packages and create ${REPO_ROOT}/.venv."
  read -r -p "Press Enter to continue or Ctrl-C to abort. "
fi

log_status "PHASE|SETUP start ${REPO_NAME}"
record_cmd "DEBIAN_FRONTEND=noninteractive apt-get update -y"
DEBIAN_FRONTEND=noninteractive apt-get update -y

PY_VER="$(${BENCHMARK_PYTHON:-python3} -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
apt_install \
  python3 python3-venv "python${PY_VER}-venv" python3-dev "python${PY_VER}-dev" python3-pip \
  build-essential g++ gcc make cmake sqlite3 jq pkg-config pciutils numactl libnuma-dev \
  curl ca-certificates ripgrep stress-ng lmbench linux-tools-common linux-tools-generic
KERNEL_RELEASE="$(uname -r || true)"
if [[ -n "${KERNEL_RELEASE}" ]]; then
  apt_install "linux-tools-${KERNEL_RELEASE}"
fi
if [[ -f src/cudnn_conv.cu ]]; then
  # scripts/build.sh only ever puts /usr/local/cuda, /usr/local/cuda-12.8,
  # and /usr/local/cuda-12.6 on PATH (no cuda-13.x), so nvcc there always
  # resolves to a CUDA 12 toolkit. Installing libcudnn9-cuda-13 alongside
  # libcudnn9-cuda-12 put two ABI-incompatible cuDNN builds on the linker
  # path; bin/cudnn_conv then aborted (SIGABRT) at runtime on whichever one
  # the loader picked, not a clean [FAIL]. Install only the variant that
  # matches the toolkit build.sh can actually select.
  apt_install libcudnn9-cuda-12 libcudnn9-headers-cuda-12 libcudnn9-dev-cuda-12
fi

if ! command -v nvcc >/dev/null 2>&1; then
  apt_install cuda-nvcc-12-8 cuda-cudart-dev-12-8 nvidia-cuda-toolkit || true
  apt_install cuda-nvcc-12-6 cuda-cudart-dev-12-6 || true
fi
export PATH="/usr/local/cuda/bin:/usr/local/cuda-13.3/bin:/usr/local/cuda-12.8/bin:/usr/local/cuda-12.6/bin:${PATH}"
if ! command -v nvcc >/dev/null 2>&1; then
  echo "[FAIL] NVCC is required and was not found after CUDA toolkit install." >&2
  exit 1
fi
if ! command -v dcgmi >/dev/null 2>&1; then
  apt_install datacenter-gpu-manager datacenter-gpu-manager-4 || true
fi

PYTHON_BIN="${BENCHMARK_PYTHON:-python3}"
if [[ ! -x "${REPO_ROOT}/.venv/bin/python" ]]; then
  log_status "STEP|SETUP create venv"
  record_cmd "${PYTHON_BIN} -m venv ${REPO_ROOT}/.venv"
  "${PYTHON_BIN}" -m venv "${REPO_ROOT}/.venv"
fi
"${REPO_ROOT}/.venv/bin/python" -m pip install --upgrade pip
if [[ -f requirements.txt ]]; then
  "${REPO_ROOT}/.venv/bin/python" -m pip install -r requirements.txt
fi
"${REPO_ROOT}/.venv/bin/python" -m pip install PyYAML

if [[ "${BENCHMARK_INSTALL_PYTORCH}" == "1" || "${BENCHMARK_INSTALL_JAX}" == "1" ]]; then
  if [[ -f scripts/install_pytorch_nvidia.sh ]]; then
    log_status "STEP|SETUP install_pytorch_nvidia.sh"
    record_cmd "bash scripts/install_pytorch_nvidia.sh"
    bash scripts/install_pytorch_nvidia.sh
    "${REPO_ROOT}/.venv/bin/python" -m pip install numpy
  else
    echo "[FAIL] Framework requires CUDA PyTorch/JAX but scripts/install_pytorch_nvidia.sh is missing." >&2
    exit 1
  fi
fi

for _helper in install_sglang_nvidia.sh install_rag_nvidia.sh install_sdxl_python.sh; do
  if [[ -f "scripts/${_helper}" ]]; then
    log_status "STEP|SETUP ${_helper}"
    record_cmd "bash scripts/${_helper}"
    bash "scripts/${_helper}"
  fi
done

verify_cmd "Bash" bash --version
verify_cmd "SQLite" sqlite3 --version
verify_cmd "Python" "${REPO_ROOT}/.venv/bin/python" --version
verify_cmd "PyYAML" "${REPO_ROOT}/.venv/bin/python" -c "import yaml; print(yaml.__version__)"
verify_cmd "CUDA Runtime" test -e /usr/local/cuda/lib64/libcudart.so -o -e /usr/local/cuda/targets/x86_64-linux/lib/libcudart.so
verify_cmd "NVCC" nvcc --version
verify_cmd "nvidia-smi" nvidia-smi
if command -v dcgmi >/dev/null 2>&1; then
  verify_cmd "NVIDIA DCGM Diagnostics" dcgmi --help
else
  log_status "WARN|SETUP dcgmi not installed; continuing with nvidia-smi stack checks"
fi
test -e /dev/nvidiactl || { echo "[FAIL] /dev/nvidiactl is not accessible." >&2; exit 1; }

if [[ -f scripts/build.sh ]]; then
  log_status "STEP|SETUP scripts/build.sh"
  bash scripts/build.sh
fi

if [[ -f src/cublas_gemm.cu && ! -x bin/cublas_gemm ]]; then
  echo "[FAIL] src/cublas_gemm.cu is present but bin/cublas_gemm was not built." >&2
  exit 1
fi
if [[ -f src/cudnn_conv.cu && ! -x bin/cudnn_conv ]]; then
  echo "[FAIL] src/cudnn_conv.cu is present but bin/cudnn_conv was not built." >&2
  exit 1
fi
if [[ -f src/stream.c && ! -x bin/stream && ! -x build/stream ]]; then
  echo "[FAIL] src/stream.c is present but the STREAM binary was not built." >&2
  exit 1
fi
if [[ -f src/numa_sweep.cpp && ! -x bin/numa_sweep ]]; then
  echo "[FAIL] src/numa_sweep.cpp is present but bin/numa_sweep was not built." >&2
  exit 1
fi
if [[ -f src/babelstream.cu && ! -x bin/babelstream ]]; then
  echo "[FAIL] src/babelstream.cu is present but bin/babelstream was not built." >&2
  exit 1
fi
if [[ -f src/ecc_walk.cu && ! -x bin/ecc_walk ]]; then
  echo "[FAIL] src/ecc_walk.cu is present but bin/ecc_walk was not built." >&2
  exit 1
fi
if [[ -f src/gups.c && ! -x bin/gups ]]; then
  echo "[FAIL] src/gups.c is present but bin/gups was not built." >&2
  exit 1
fi
if [[ -f src/cuda_memcpy.cu && ! -x bin/cuda_memcpy ]]; then
  echo "[FAIL] src/cuda_memcpy.cu is present but bin/cuda_memcpy was not built." >&2
  exit 1
fi
if [[ -f src/nccl_bw.cu && ! -x bin/nccl_bw ]]; then
  echo "[FAIL] src/nccl_bw.cu is present but bin/nccl_bw was not built." >&2
  exit 1
fi
if [[ -f src/nvhpl.cu && ! -x bin/nvhpl ]]; then
  echo "[FAIL] src/nvhpl.cu is present but bin/nvhpl was not built." >&2
  exit 1
fi

printf 'setup_complete=1\nworkload=%s\ncompleted_at=%s\n' "${REPO_NAME}" "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" > "${REPO_ROOT}/.setup_state"
log_status "PHASE|SETUP complete"
echo "[PASS] setup.sh complete"
wall "setup.sh now complete" >/dev/null 2>&1 || true
