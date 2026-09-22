#!/usr/bin/env bash
# File: scripts/lib/common.sh
# Version: 1.2.2
# Maintainer: AI Agent GPU Benchmark Repo Generator
# Date: 2026-08-28
# Description: Shared logging, command execution, metadata, secret-masking, ledger-on-die, summary command lines, HTTP ready-wait helpers, and hipcc host-GCC pin.
# Execution: source scripts/lib/common.sh
# Options: None
# Requirements: bash 4+
# Environment: Local benchmark host.
# Dependencies: coreutils, uname, hostname; journalctl when available
# Variables: LOG_LEVEL, RUN_DIR, COMMAND_LOG, BENCHMARK_PROFILE, BENCHMARK_START_DATETIME, BENCHMARK_RUN_ACTIVE, BENCHMARK_RUN_COMMAND, BENCHMARK_RUN_COMMAND_SUBMITTED, BENCHMARK_READY_WAIT_SEC
# Repository: gpu-bench/sys-bench template
# License: Apache-2.0

set -euo pipefail

LOG_LEVEL="${LOG_LEVEL:-INFO}"

# Keep Hugging Face snapshots and pip wheels on the overlay-root home when
# the workload tree lives on a quotaed volume (this pod: /workspace ~35G).
# Overlay run_benchmark.sh files use ${HF_HOME:-${REPO_ROOT}/.cache/...}, so
# exporting HF_HOME here redirects weights without editing those overlays.
if [[ -z "${HF_HOME:-}" ]]; then
  export HF_HOME="${HOME}/.cache/huggingface"
fi
if [[ -z "${PIP_CACHE_DIR:-}" ]]; then
  export PIP_CACHE_DIR="${HOME}/.cache/pip"
fi

# hipcc on Ubuntu 26.04 / ROCm 7.14 (Clang 23) prefers GCC 16, which does
# not expose <cstdlib> to the HIP wrapper. Export HIPCC_COMPILE_FLAGS_APPEND
# so child `bash scripts/build.sh` from setup and collect inherits the pin.
if [[ -f "${BASH_SOURCE[0]%/*}/hipcc_host_gcc.sh" ]]; then
  # shellcheck disable=SC1091
  source "${BASH_SOURCE[0]%/*}/hipcc_host_gcc.sh"
fi

timestamp_utc() {
  date -u +"%Y-%m-%d %H:%M:%S"
}

iso_utc_now() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

log_msg() {
  local level="$1"
  shift
  log "$level" "$*"
}

set_log_level() {
  LOG_LEVEL="${1:-INFO}"
  export LOG_LEVEL
}

log_phase() {
  log_msg INFO "Phase: $*"
}

log_section() {
  log_msg INFO "========== $* =========="
}

log() {
  local level="$1"
  shift
  case "${level}" in
    ERROR|FAIL) log_fail "$*" ;;
    WARN) log_warn "$*" ;;
    INFO) log_info "$*" ;;
    PASS) log_pass "$*" ;;
    *) echo "[${level}] $*" ;;
  esac
}

run_cmd() {
  if [[ "$#" -eq 1 ]]; then
    printf '[RUN] %s\n' "$1"
    bash -lc "$1"
  else
    printf '[RUN] %q ' "$@"
    printf '\n'
    "$@"
  fi
}

run_logged_cmd() {
  run_cmd "$@"
}

ensure_file_header() {
  local target="$1"
  [[ -e "${target}" ]] || : > "${target}"
}

log_error() { echo "[ERROR] $*" >&2; }
log_warn() { echo "[WARN] $*" >&2; }
log_info() { [[ "${LOG_LEVEL}" != "ERROR" && "${LOG_LEVEL}" != "WARN" ]] && echo "[INFO] $*" || true; }
log_pass() { echo "[PASS] $*"; }
log_fail() { echo "[FAIL] $*" >&2; }

benchmark_run_err_trap() {
  local line="${1:-unknown}"
  local cmd="${2:-unknown}"
  # set -e abort that never called die() (102 validation is the usual case).
  # Still exit 1. This does not turn a failure into success.
  append_runtime_ledger_on_error "set -e exit at line ${line}: ${cmd}" || true
  exit 1
}

begin_benchmark_run() {
  BENCHMARK_PROFILE="${1:-${BENCHMARK_PROFILE:-smoke}}"
  BENCHMARK_START_DATETIME="${2:-${BENCHMARK_START_DATETIME:-$(iso_utc_now)}}"
  BENCHMARK_RUN_ACTIVE=1
  BENCHMARK_LEDGER_WRITTEN=0
  export BENCHMARK_PROFILE BENCHMARK_START_DATETIME BENCHMARK_RUN_ACTIVE BENCHMARK_LEDGER_WRITTEN
  # Without errtrace, ERR is not inherited by functions. 102's validate_phase
  # then exits 1 under set -e and never writes a ledger row.
  set -E
  trap 'benchmark_run_err_trap "${LINENO}" "${BASH_COMMAND}"' ERR
}

isolate_repo_python() {
  # Stop 131 from importing 130's editable sglang/aiter via inherited PYTHONPATH.
  unset PYTHONPATH
  unset PYTHONHOME
  export PYTHONNOUSERSITE=1
}

set_benchmark_run_dir() {
  BENCHMARK_RUN_DIR="${1:-}"
  export BENCHMARK_RUN_DIR
}

capture_benchmark_run_command_submitted() {
  local quoted=""
  BENCHMARK_RUN_COMMAND_SUBMITTED="bash run_benchmark.sh"
  if (($#)); then
    printf -v quoted ' %q' "$@"
    BENCHMARK_RUN_COMMAND_SUBMITTED+="${quoted}"
  fi
  export BENCHMARK_RUN_COMMAND_SUBMITTED
}

set_benchmark_run_command_submitted() {
  BENCHMARK_RUN_COMMAND_SUBMITTED="${1:-}"
  export BENCHMARK_RUN_COMMAND_SUBMITTED
}

set_benchmark_run_command() {
  BENCHMARK_RUN_COMMAND="${1:-}"
  export BENCHMARK_RUN_COMMAND
}

set_benchmark_run_command_fully_resolved() {
  set_benchmark_run_command "$@"
}

print_benchmark_summary_commands() {
  printf '[INFO] Command submitted: %s\n' "${BENCHMARK_RUN_COMMAND_SUBMITTED:-}"
  printf '[INFO] Command fully resolved: %s\n' "${BENCHMARK_RUN_COMMAND:-}"
}

write_metrics_summary_txt() {
  local dest="${RUN_DIR:?RUN_DIR is required}/metrics_summary.txt"
  local python_bin="${PYTHON_BIN:-python3}"
  local summary_path="${REPO_ROOT:-.}/results/summary.json"
  local start="${START_ISO:-${BENCHMARK_START_DATETIME:-}}"
  local stop="${STOP_ISO:-${STOP_TIME:-}}"
  local run_id="" status="ok" samples="0"
  if [[ -f "${summary_path}" ]]; then
    run_id="$("${python_bin}" -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8")).get("run_id",""))' "${summary_path}")"
    status="$("${python_bin}" -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8")).get("status","ok"))' "${summary_path}")"
    samples="$("${python_bin}" -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8")).get("sample_count",0))' "${summary_path}")"
  fi
  {
    echo "===== Benchmark Summary ====="
    echo "Run ID: ${run_id} | Status: ${status} | Samples: ${samples} | Profile: ${PROFILE:-} | Device: ${DEVICE:-}"
    echo "Command submitted: ${BENCHMARK_RUN_COMMAND_SUBMITTED:-}"
    echo "Command fully resolved: ${BENCHMARK_RUN_COMMAND:-}"
    echo "Start time: ${start}"
    echo "Stop time: ${stop}"
    echo "Elapsed time: ${ELAPSED:-0} sec"
    echo "Artifacts: ${RUN_DIR}"
    echo "SQLite DB: ${REPO_ROOT}/results/benchmark.db"
    echo
    if [[ -f scripts/print_metric_summary.py && -f "${summary_path}" ]]; then
      "${python_bin}" scripts/print_metric_summary.py --definition benchmark_specification.json --summary "${summary_path}" | sed 's/^\[INFO\] //'
    fi
    echo
  } > "${dest}"
}

finish_benchmark_run() {
  trap - ERR
  set +E
  BENCHMARK_LEDGER_WRITTEN=1
  BENCHMARK_RUN_ACTIVE=0
}

append_runtime_ledger_on_error() {
  local notes="${1:-error}"
  local python_bin=""
  local start=""
  local start_epoch=""
  local now_epoch=""
  local elapsed=0
  [[ "${BENCHMARK_RUN_ACTIVE:-0}" == "1" ]] || return 0
  [[ "${BENCHMARK_LEDGER_WRITTEN:-0}" != "1" ]] || return 0
  if [[ -x "${REPO_ROOT:-.}/.venv/bin/python" ]]; then
    python_bin="${REPO_ROOT:-.}/.venv/bin/python"
  else
    python_bin="${PYTHON_BIN:-python3}"
  fi
  [[ -f scripts/update_runtime_ledger.py ]] || return 0
  start="${BENCHMARK_START_DATETIME:-$(iso_utc_now)}"
  start_epoch="$(date -u -d "${start}" +%s 2>/dev/null || true)"
  now_epoch="$(date -u +%s)"
  if [[ -n "${start_epoch}" ]]; then
    elapsed=$((now_epoch - start_epoch))
    if (( elapsed < 0 )); then
      elapsed=0
    fi
  fi
  local raw_dir="${BENCHMARK_RUN_DIR:-${RUN_DIR:-}}"
  local extra_args=()
  if [[ -n "${raw_dir}" && -f "${raw_dir}/run.log" ]]; then
    extra_args+=(--run-log "${raw_dir}/run.log")
  fi
  if [[ -n "${raw_dir}" && -f "${raw_dir}/commands_executed.sh" ]]; then
    extra_args+=(--command-log "${raw_dir}/commands_executed.sh")
  fi
  "${python_bin}" scripts/update_runtime_ledger.py \
    --profile "${BENCHMARK_PROFILE:-smoke}" \
    --start-datetime "${start}" \
    --total-runtime "${elapsed}" \
    --exit-code 1 \
    --failure-detail "${notes}" \
    --raw-run-dir "${raw_dir}" \
    --runtime-root "${REPO_ROOT:-$(pwd)}" \
    --run-benchmark-command-submitted "${BENCHMARK_RUN_COMMAND_SUBMITTED:-}" \
    --run-benchmark-command-fully-resolved "${BENCHMARK_RUN_COMMAND:-}" \
    --notes "${notes}" \
    "${extra_args[@]}" || log_warn "Runtime ledger update failed"
  BENCHMARK_LEDGER_WRITTEN=1
}

die() {
  log_error "$*"
  append_runtime_ledger_on_error "$*" || true
  exit 1
}

wait_for_server() {
  local url="$1"
  local timeout_sec="${2:-${BENCHMARK_READY_WAIT_SEC:-600}}"
  local elapsed=0
  local code=""
  [[ -n "${url}" ]] || die "wait_for_server requires a URL"
  log_info "Waiting up to ${timeout_sec}s for ${url} (HTTP 503 is not ready)"
  while (( elapsed < timeout_sec )); do
    if [[ -n "${SERVER_PID:-}" ]] && ! kill -0 "${SERVER_PID}" 2>/dev/null; then
      die "Server process ${SERVER_PID} exited before ready at ${url} (last HTTP ${code:-none})"
    fi
    code="$(curl -sS -o /dev/null -w '%{http_code}' --connect-timeout 2 --max-time 5 "${url}" 2>/dev/null || true)"
    if [[ "${code}" == "200" ]]; then
      log_info "Server ready at ${url} after ${elapsed}s"
      return 0
    fi
    sleep 2
    elapsed=$((elapsed + 2))
  done
  die "Server did not become ready at ${url} within ${timeout_sec}s (last HTTP ${code:-none})"
}

run_logged() {
  local command_text="$*"
  echo "[RUN] ${command_text}"
  if [[ -n "${COMMAND_LOG:-}" ]]; then
    printf '%s\n' "${command_text}" >> "${COMMAND_LOG}"
  fi
  bash -lc "${command_text}"
}

mask_environment() {
  local output_path="$1"
  env | sort | awk -F= '
    BEGIN { IGNORECASE=1 }
    $1 ~ /(TOKEN|SECRET|KEY|PASSWORD|CREDENTIAL|AUTH)/ { print $1"=<masked>"; next }
    { print }
  ' > "${output_path}"
}

# Save journalctl entries at priority warning or higher into journal_warnings.txt.
# Prefer a run window: capture_journal_warnings <run_dir> <since_iso_utc> <until_iso_utc>
# When since/until are omitted, limit to the current boot (-b) to avoid the full journal.
capture_journal_warnings() {
  local run_dir="$1"
  local since="${2:-}"
  local until="${3:-}"
  local out_path="${run_dir}/journal_warnings.txt"
  local -a journal_args

  mkdir -p "${run_dir}"
  if ! command -v journalctl >/dev/null 2>&1; then
    {
      echo "# journalctl unavailable on this host"
      echo "status=unavailable"
    } > "${out_path}"
    return 0
  fi

  journal_args=(-p warning --no-pager -o short-iso)
  if [[ -n "${since}" ]]; then
    journal_args+=(--since="${since}")
  fi
  if [[ -n "${until}" ]]; then
    journal_args+=(--until="${until}")
  fi
  if [[ -z "${since}" && -z "${until}" ]]; then
    journal_args+=(-b)
  fi

  {
    echo "# journalctl -p warning (warning and higher)"
    if [[ -n "${since}" ]]; then
      echo "# since=${since}"
    fi
    if [[ -n "${until}" ]]; then
      echo "# until=${until}"
    fi
    if [[ -z "${since}" && -z "${until}" ]]; then
      echo "# scope=current-boot"
    fi
    journalctl "${journal_args[@]}" 2>&1 || true
  } > "${out_path}"
}

capture_basic_metadata() {
  local run_dir="$1"
  mkdir -p "${run_dir}"
  mask_environment "${run_dir}/env_variables.txt"
}
