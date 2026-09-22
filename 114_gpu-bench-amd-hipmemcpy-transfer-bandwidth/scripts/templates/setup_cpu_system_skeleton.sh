#!/usr/bin/env bash
# File: scripts/templates/setup_cpu_system_skeleton.sh
# Description: Host-only setup.sh for Execution Domain CPU / System. Apt, venv, Framework tools, build.sh.
# Execution: Copied to generated repo root as setup.sh.
set -euo pipefail

if [[ -z "${HOME:-}" ]]; then
  HOME="$(getent passwd "$(id -u)" | cut -d: -f6 2>/dev/null || true)"
  HOME="${HOME:-/root}"
  export HOME
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_NAME="$(basename "${REPO_ROOT}")"
cd "${REPO_ROOT}"

ASSUME_YES=0
usage() {
  cat <<'USAGE'
Usage: bash setup.sh [OPTIONS]

Install host prerequisites for a CPU / System workload.

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
      log_status "STEP already present: ${pkg}"
      continue
    fi
    log_status "STEP apt-get install ${pkg}"
    record_cmd "DEBIAN_FRONTEND=noninteractive apt-get install -y ${pkg}"
    DEBIAN_FRONTEND=noninteractive apt-get install -y "${pkg}"
  done
}

verify_cmd() {
  local name="$1"
  shift
  if ! "$@"; then
    echo "[FAIL] Required framework item failed verification: ${name}" >&2
    exit 1
  fi
  log_status "PASS verified ${name}"
}

workload_framework=""
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
fi

if [[ "${ASSUME_YES}" -ne 1 ]]; then
  echo "setup.sh will install Ubuntu packages and create ${REPO_ROOT}/.venv."
  read -r -p "Press Enter to continue or Ctrl-C to abort. "
fi

log_status "PHASE setup.sh start ${REPO_NAME}"
record_cmd "DEBIAN_FRONTEND=noninteractive apt-get update -y"
DEBIAN_FRONTEND=noninteractive apt-get update -y

PY_VER="$(${BENCHMARK_PYTHON:-python3} -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
apt_install \
  python3 python3-venv "python${PY_VER}-venv" python3-pip \
  build-essential gcc g++ make cmake sqlite3 pkg-config \
  numactl libnuma-dev git curl ca-certificates

if grep -Eiq 'fio|flexible i/o' <<< "${workload_framework}"; then
  apt_install fio libaio-dev || apt_install fio
fi
if grep -Eiq 'iperf3' <<< "${workload_framework}"; then
  apt_install iperf3
fi
if grep -Eiq 'stress-ng' <<< "${workload_framework}"; then
  apt_install stress-ng
fi
if grep -Eiq 'lmbench' <<< "${workload_framework}"; then
  apt_install lmbench || true
fi
if grep -Eiq '(^|[,[:space:]])perf([,[:space:]]|$)|linux perf|pmu' <<< "${workload_framework}"; then
  apt_install linux-tools-common linux-tools-generic || true
  KERNEL_RELEASE="$(uname -r || true)"
  if [[ -n "${KERNEL_RELEASE}" ]]; then
    apt_install "linux-tools-${KERNEL_RELEASE}" || true
  fi
fi

PYTHON_BIN="${BENCHMARK_PYTHON:-python3}"
if [[ ! -x "${REPO_ROOT}/.venv/bin/python" ]]; then
  log_status "STEP python created ${REPO_ROOT}/.venv"
  record_cmd "${PYTHON_BIN} -m venv ${REPO_ROOT}/.venv"
  "${PYTHON_BIN}" -m venv "${REPO_ROOT}/.venv"
fi
"${REPO_ROOT}/.venv/bin/python" -m pip install --upgrade pip
if [[ -f requirements.txt ]]; then
  "${REPO_ROOT}/.venv/bin/python" -m pip install -r requirements.txt
fi
"${REPO_ROOT}/.venv/bin/python" -m pip install 'PyYAML>=6.0'

verify_cmd "Bash" bash --version
verify_cmd "SQLite" sqlite3 --version
verify_cmd "Python" "${REPO_ROOT}/.venv/bin/python" --version
verify_cmd "PyYAML" "${REPO_ROOT}/.venv/bin/python" -c "import yaml; print(yaml.__version__)"
if grep -Eiq 'fio|flexible i/o' <<< "${workload_framework}"; then
  verify_cmd "fio" fio --version
fi
if grep -Eiq 'iperf3' <<< "${workload_framework}"; then
  verify_cmd "iperf3" iperf3 --version
fi
if grep -Eiq 'stress-ng' <<< "${workload_framework}"; then
  verify_cmd "stress-ng" stress-ng --version
fi

if [[ -f scripts/build.sh ]]; then
  log_status "STEP scripts/build.sh"
  bash scripts/build.sh
fi
if [[ -f src/stream.c && ! -x bin/stream && ! -x build/stream ]]; then
  echo "[FAIL] src/stream.c is present but the STREAM binary was not built." >&2
  exit 1
fi
if [[ -f src/numa_sweep.cpp && ! -x bin/numa_sweep ]]; then
  echo "[FAIL] src/numa_sweep.cpp is present but bin/numa_sweep was not built." >&2
  exit 1
fi
if [[ -f src/gups.c && ! -x bin/gups ]]; then
  echo "[FAIL] src/gups.c is present but bin/gups was not built." >&2
  exit 1
fi

printf 'setup_complete=1\nworkload=%s\nbundle=cpu-system\ncompleted_at=%s\n' \
  "${REPO_NAME}" "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" > "${REPO_ROOT}/.setup_state"
log_status "PHASE SETUP complete"
echo "[PASS] setup.sh complete"
wall "setup.sh now complete" >/dev/null 2>&1 || true
