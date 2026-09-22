#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import io
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml


def pv(params, key, profile, default=""):
    raw = params.get(key, default)
    if isinstance(raw, dict):
        return raw.get(profile, raw.get("smoke", default))
    return default if raw is None else raw


def as_list(value):
    return [p.strip() for p in str(value or "").replace(";", ",").split(",") if p.strip()]


def duration_seconds(raw):
    try:
        number = float(raw)
    except (TypeError, ValueError):
        return 5.0
    return number / 1000.0 if number >= 10000 else number


def load_params(path):
    cfg = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return cfg.get("sweep") or {}


def write_csv(path, header, rows):
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=header, extrasaction="ignore", lineterminator=chr(10))
    writer.writeheader()
    rows = list(rows)
    if len(rows) == 1:
        rows.append(dict(rows[0]))
    for index, row in enumerate(rows):
        writer.writerow({"sample_index": index, **row})
    text = buf.getvalue()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8")
    print(text, end="")
    return text


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--raw-file", required=True)
    parser.add_argument("--profile", default="smoke")
    parser.add_argument("--config", default="config/benchmark_config.yaml")
    parser.add_argument("--device", default="gpu")
    parser.add_argument("--output-format", default="csv")
    return parser.parse_args()

def run_command(command):
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
    except FileNotFoundError:
        return 127, f"missing:{command[0]}"
    return completed.returncode, (completed.stdout or "") + "\n" + (completed.stderr or "")


def package_version(name):
    completed = subprocess.run(["dpkg-query", "-W", "-f=${Version}", name], check=False, capture_output=True, text=True)
    return (completed.stdout or "").strip() if completed.returncode == 0 else ""


def main() -> int:
    args = parse_args()
    sweep = load_params(args.config)
    expected_kernel = str(sweep.get("kernel_version", "6.8.0"))
    expected_driver = str(sweep.get("driver_version", "6"))
    expected_rocm = str(sweep.get("rocm_version", "7.2.1"))
    packages = [item.strip() for item in str(sweep.get("required_packages", "rocm-core,rocm-smi")).split(",") if item.strip()]
    permissions_check = str(sweep.get("permissions_check", "true")).lower() in {"1", "true", "yes"}
    uname = os.uname().release
    kernel_mismatch = 0 if expected_kernel.split("-")[0] in uname or uname.startswith(expected_kernel) else 1
    amdgpu = run_command(["modinfo", "amdgpu"])[1]
    driver_ok = expected_driver in amdgpu
    driver_mismatch = 0 if driver_ok else 1
    aliases = {"rocm-smi": ["rocm-smi", "rocm-smi-lib"], "amd-smi": ["amd-smi", "amd-smi-lib"]}
    package_mismatch = 0
    for name in packages:
        version = ""
        for candidate in aliases.get(name, [name]):
            version = package_version(candidate)
            if version:
                break
        if not version:
            package_mismatch += 1
    permission_errors = 0
    if permissions_check:
        for node in (Path("/dev/kfd"), Path("/dev/dri/renderD128")):
            if node.exists() and not os.access(node, os.R_OK):
                permission_errors += 1
        if not Path("/dev/kfd").exists() and not Path("/dev/dri/renderD128").exists():
            permission_errors += 1
    firmware_ok = 100.0 if "firmware" in amdgpu.lower() or Path("/lib/firmware/amdgpu").exists() else 0.0
    Path(args.run_dir).mkdir(parents=True, exist_ok=True)
    checks = []
    for command in (["rvs", "--version"], ["rocminfo"], ["rocm-smi"], ["amd-smi", "static"], ["uname", "-a"], ["modinfo", "amdgpu"], ["hipcc", "--version"]):
        checks.append((command[0], *run_command(command)))
    header = ["sample_index", "check_name", "rocm_package_mismatch_count", "kernel_driver_mismatch_count", "firmware_compliance_percent", "driver_compliance_percent", "permission_error_count"]
    rows = []
    for name, code, text in checks:
        extra_pkg = package_mismatch + (1 if code != 0 and name in {"rvs", "rocminfo", "rocm-smi", "amd-smi", "hipcc"} else 0)
        rows.append({
            "check_name": name,
            "rocm_package_mismatch_count": float(extra_pkg),
            "kernel_driver_mismatch_count": float(driver_mismatch + (1 if name == "modinfo" and code != 0 else 0)),
            "firmware_compliance_percent": firmware_ok if code == 0 else 0.0,
            "driver_compliance_percent": 100.0 if driver_mismatch == 0 and (code == 0 or name in {"uname"}) else 0.0,
            "permission_error_count": float(permission_errors),
        })
        (Path(args.run_dir) / f"{name}.txt").write_text(text, encoding="utf-8")
    write_csv(args.raw_file, header, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
