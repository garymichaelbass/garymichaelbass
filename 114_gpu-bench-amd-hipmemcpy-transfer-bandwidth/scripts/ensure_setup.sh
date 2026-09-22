#!/usr/bin/env bash
# File: scripts/ensure_setup.sh
# Description: Basic setup-on-demand guard for run_benchmark.sh.
# Execution: bash scripts/ensure_setup.sh
# Note: Reboot-driven setup must finish after reboot before run_benchmark.sh is rerun.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

if [[ -f .setup_state ]]; then
    if [[ ! -x "${REPO_ROOT}/.venv/bin/python" ]]; then
        printf '[WARN] .setup_state exists but .venv python is missing; re-running setup.\n'
        rm -f .setup_state
    else
        printf '[PASS] Setup already complete: %s\n' "${REPO_ROOT}"
        exit 0
    fi
fi

[[ -f setup.sh ]] || {
    printf '[ERROR] setup.sh is missing; cannot start automatic setup.\n' >&2
    exit 1
}

printf '[INFO] .setup_state is absent; starting automatic setup.\n'
setup_args=()
if grep -Fq -- "--assume-yes" setup.sh; then
    setup_args+=(--assume-yes)
fi

if ! bash setup.sh "${setup_args[@]}"; then
    printf '[ERROR] Automatic setup failed; benchmark will not run.\n' >&2
    exit 1
fi

if [[ ! -f .setup_state ]]; then
    if command -v systemctl >/dev/null 2>&1 &&
       systemctl list-unit-files --type=service --no-legend 2>/dev/null |
       grep -Eq '[^[:space:]]+-setup-resume\.service'; then
        printf '[WARN] Setup is awaiting reboot-resume completion. Rerun bash run_benchmark.sh after setup completes.\n' >&2
    else
        printf '[ERROR] setup.sh returned successfully without creating .setup_state; benchmark will not run.\n' >&2
    fi
    exit 1
fi

printf '[PASS] Automatic setup completed: %s\n' "${REPO_ROOT}"
