# PRD.md:  "The Why"; Product requirements, benchmark metadata table, high-level requirements, etc.

Product Requirements Document

"The Why"; Product requirements, benchmark metadata table, high-level requirements, etc. Defines the benchmark goal, validation objective, test name, benchmark number, category, and high-level success criteria.

## Benchmark Matrix Document Metadata (via benchmark_specification.json)

This PRD.md section is populated from benchmark_specification.json, which is the structured source of benchmark-specific product requirements.

## Workload Number
128

## Workload Name
vLLM Inference Throughput & Latency

## Execution Summary (Run and Measure)
Launch tiny_kv_server.py or python -m vllm.entrypoints.openai.api_server --dtype bfloat16 on 127.0.0.1:8000, wait for /v1/models, run concurrent benchmark_serving.py completions with yaml input_len/output_len/max_concurrency, and write throughput plus TTFT/TPOT/ITL/E2E columns to raw_results.csv, to measure vLLM serving performance

## Main Goal
Measure vLLM serving throughput and latency

## Validation Objective
Validates raw_results.csv throughput and latency columns. Smoke uses tiny_kv_server.py

## Workload Category
LLM Inference & Serving


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
