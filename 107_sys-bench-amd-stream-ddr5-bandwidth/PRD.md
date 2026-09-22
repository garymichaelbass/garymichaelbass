# PRD.md:  "The Why"; Product requirements, benchmark metadata table, high-level requirements, etc.

Product Requirements Document

"The Why"; Product requirements, benchmark metadata table, high-level requirements, etc. Defines the benchmark goal, validation objective, test name, benchmark number, category, and high-level success criteria.

## Benchmark Matrix Document Metadata (via benchmark_specification.json)

This PRD.md section is populated from benchmark_specification.json, which is the structured source of benchmark-specific product requirements.

## Workload Number
107

## Workload Name
STREAM - CPU (Copy/Scale/Add/Triad

## Execution Summary (Run and Measure)
Compile official STREAM src/stream.c with gcc -O3 -fopenmp, run build/stream under OMP_NUM_THREADS, parse Copy/Scale/Add/Triad Best Rate MB/s, convert to GB/s, and compute triad/400 efficiency, to measure CPU STREAM bandwidth. numactl is not used

## Main Goal
Measure sustained CPU STREAM bandwidth

## Validation Objective
Validates Copy/Scale/Add/Triad Best Rate parse and triad/400 efficiency. numactl pinning is not applied

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
