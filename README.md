# SQL-Trap-Eval 🛡️🕳️

`sql-trap-eval` is an open-source adversarial evaluation benchmark and test runner designed to detect silent semantic failures, logical traps, and hallucinations in Large Language Model (LLM) generated SQL queries.

## 🎯 The Problem
Standard Text-to-SQL benchmarks only evaluate syntax validity or exact string matches. However, LLMs frequently generate syntactically valid SQL queries that contain **silent semantic errors** (e.g., NULL poisoning in subqueries, column omission in aggregate functions, or unintended Cartesian products). These bugs pass standard test suites but corrupt production data.

## 🛠️ Benchmark Traps Included
1. **TRAP-001 (`NOT IN` + `NULL` Subquery)**: Unaware that a single `NULL` value in a subquery poisons the `NOT IN` operator, causing it to return zero rows.
2. **TRAP-002 (`COUNT(column)` vs `COUNT(*)` Silent Omission)**: Using `COUNT(column)` which silently ignores rows where the column is `NULL`, leading to undercounting.
3. **TRAP-003 (Implicit Cartesian Product / Cross Join)**: Omitting join conditions (`ON`), creating an unintended cross join that multiplies row counts.

## 🚀 Quickstart

### 1. Run the Evaluation Suite
```bash
python eval_harness.py