# PRD.md:  "The Why"; Product requirements, benchmark metadata table, high-level requirements, etc.

Product Requirements Document

"The Why"; Product requirements, benchmark metadata table, high-level requirements, etc. Defines the benchmark goal, validation objective, test name, benchmark number, category, and high-level success criteria.

## Benchmark Matrix Document Metadata (via benchmark_specification.json)

This PRD.md section is populated from benchmark_specification.json, which is the structured source of benchmark-specific product requirements.

## Workload Number
114

## Workload Name
hipMemcpy Bandwidth Test (H2D, D2H, D2D

## Execution Summary (Run and Measure)
Compile and run bin/hip_memcpy_bw with yaml direction, pinned_memory, min_bytes, max_bytes, step_factor, and iteration counts, then parse one row per direction and transfer size, to measure HIP copy bandwidth and latency

## Main Goal
Measure HIP H2D/D2H/D2D transfer bandwidth

## Validation Objective
Validates one CSV row per direction and transfer size from bin/hip_memcpy_bw

## Workload Category
Memory, Bandwidth & Data Movement


## Validation Requirement

The benchmark must include an automated SQLite-integrated validation layer that verifies persisted results from `results/benchmark.db`. Validation must confirm:

1. The benchmark run completed successfully with no tool errors.
2. Required samples and aggregate metrics were persisted for every swept shape.
3. Metrics are finite and physically sensible (positive, within plausible bounds).
4. Measured values satisfy configured thresholds when the workload defines pass/fail gates.
5. The benchmark fails validation when required data is missing, invalid, or outside bounds.


## Non-Functional Requirements

| Requirement | Target |
|---|---|
| Automation | Runs to completion without manual intervention after `bash run_benchmark.sh` |
| Idempotency | Re-running `run_benchmark.sh` appends a new run; never corrupts existing rows |
| Persistence | All metrics survive script exit; `results/benchmark.db` is the durable record |
