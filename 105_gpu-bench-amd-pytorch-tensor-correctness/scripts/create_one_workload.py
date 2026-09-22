#!/usr/bin/env python3
# File: scripts/create_one_workload.py
# Description: Official sequential create → remote-validate → record driver for one or more workloads.
# Execution: python3 scripts/create_one_workload.py --prompt-file <PROMPT> --workload 106
# Do not call create_generated_batch.py from the chatbox path.
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TEMPLATE_COPY_SUFFIX = "_copy"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create, remotely validate, and record workloads one at a time")
    parser.add_argument("--workload", action="append", default=[], help="Workload number; repeat or pass several")
    parser.add_argument("workloads", nargs="*", help="Additional workload numbers")
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--template-root", default=".")
    parser.add_argument("--project-root", default="")
    parser.add_argument("--skip-remote-refresh", action="store_true", default=True)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def _ssh_target(prompt_path: Path) -> str:
    text = prompt_path.read_text(encoding="utf-8")
    match = re.search(r"(ssh(?:\s+-i\s+\S+)?[^\n]*@\d{1,3}(?:\.\d{1,3}){3})", text, flags=re.I)
    return match.group(1).strip() if match else ""


def _duration(started: str, finished: str) -> str:
    start_dt = datetime.fromisoformat(started.replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(finished.replace("Z", "+00:00"))
    total = max(0, int((end_dt - start_dt).total_seconds()))
    mins, secs = divmod(total, 60)
    return f"{mins}m {secs:02d}s"


def record(project_root: Path, workload: str, repo_name: str, status: str, started: str, finished: str, note: str) -> None:
    path = project_root / "batch_generation_manifest.json"
    batch = {"schema_version": "1.0.0", "repositories": []}
    if path.is_file():
        batch = json.loads(path.read_text(encoding="utf-8"))
    batch["repositories"] = [row for row in batch.get("repositories", []) if str(row.get("workload")) != workload]
    batch.setdefault("repositories", []).append(
        {
            "workload": workload,
            "repo_name": repo_name,
            "repo_path": f"{workload}_{repo_name}",
            "status": status,
            "create_start_time": started,
            "create_end_time": finished,
            "create_total_time": _duration(started, finished),
            "notes": note,
        }
    )
    path.write_text(json.dumps(batch, indent=2) + "\n", encoding="utf-8")
    print(f"[RECORD] {workload} {status} {_duration(started, finished)}", flush=True)


def remote_validate(ssh: str, repo_dir: Path) -> int:
    if not ssh:
        print("[INFO] No SSH target in prompt; skipping remote validation", flush=True)
        return 0
    name = repo_dir.name
    copy = subprocess.run(
        [
            "bash",
            "-lc",
            (
                f"tar -cf - {name} | {ssh} "
                f"'rm -rf /root/{name} && tar --no-same-owner -xf - -C /root && "
                f"find /root/{name} -type d -exec chmod 755 {{}} + && echo COPY_OK'"
            ),
        ],
        cwd=str(repo_dir.parent),
        check=False,
    )
    if copy.returncode != 0:
        print("[FAIL] remote copy failed", flush=True)
        return copy.returncode
    script = f"""
set -euo pipefail
REPO=/root/{name}
cd "$REPO"
# Windows tar extracts as 0777 (ls lime-green / other-writable). Directories must be 0755.
find "$REPO" -type d -exec chmod 755 {{}} +
find "$REPO" -type f -exec chmod 644 {{}} +
find "$REPO" -type f \\( -name '*.sh' -o -name '*.py' -o -name '*.md' -o -name '*.yaml' -o -name '*.json' -o -name '*.txt' \\) ! -path '*/third_party/*' -print0 | xargs -0 sed -i 's/\\r$//'
chmod +x "$REPO"/*.sh "$REPO"/scripts/*.sh "$REPO"/scripts/lib/*.sh 2>/dev/null || true
bash setup.sh --assume-yes
bash run_benchmark.sh --profile smoke --validate
bash scripts/self_check_generated_repo.sh
bash scripts/check_github_publish_ready.sh
echo REMOTE_OK
"""
    return subprocess.run(ssh.split() + [script], check=False).returncode


def process_one(workload: str, args: argparse.Namespace, template_root: Path, project_root: Path, ssh: str) -> int:
    started = utc_now()
    repo_name = "unknown"
    print(f"[START] workload {workload} at {started}", flush=True)
    try:
        command = [
            sys.executable,
            str(template_root / "scripts" / "create_generated_repo.py"),
            "--prompt-file",
            str(Path(args.prompt_file).resolve()),
            "--workload",
            workload,
            "--template-root",
            str(template_root),
            "--project-root",
            str(project_root),
        ]
        if args.force:
            command.append("--force")
        if args.skip_remote_refresh:
            command.append("--skip-remote-refresh")
        created = subprocess.run(command, cwd=str(template_root), check=False)
        if created.returncode != 0:
            raise RuntimeError(f"create_generated_repo.py exited {created.returncode}")
        candidates = [path for path in project_root.iterdir() if path.is_dir() and path.name.startswith(f"{workload}_")]
        if not candidates:
            raise RuntimeError(f"no repository directory for workload {workload}")
        repo = candidates[0]
        spec = json.loads((repo / "benchmark_specification.json").read_text(encoding="utf-8"))
        fields = {str(item.get("field_name", "")): str(item.get("value", "") or "") for item in spec}
        repo_name = fields.get("Repo Name") or repo.name.split("_", 1)[-1]
        rc = remote_validate(ssh, repo)
        finished = utc_now()
        record(project_root, workload, repo_name, "passed" if rc == 0 else "failed", started, finished, "" if rc == 0 else f"remote rc={rc}")
        return rc
    except Exception as exc:
        finished = utc_now()
        record(project_root, workload, repo_name, "failed", started, finished, str(exc)[:300])
        print(f"[FAIL] {workload}: {exc}", flush=True)
        return 1


def main() -> int:
    args = parse_args()
    template_root = Path(args.template_root).resolve()
    project_root = Path(args.project_root).resolve() if args.project_root else template_root.parent
    prompt = Path(args.prompt_file).resolve()
    workloads = [str(item) for item in (args.workload or []) + list(args.workloads)]
    if not workloads:
        raise SystemExit("usage: create_one_workload.py --prompt-file <file> --workload <N> [<N>...]")
    ssh = _ssh_target(prompt)
    rc = 0
    for workload in workloads:
        item_rc = process_one(str(workload), args, template_root, project_root, ssh)
        if item_rc != 0:
            rc = item_rc
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
