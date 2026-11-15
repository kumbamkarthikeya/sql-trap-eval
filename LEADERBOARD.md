# 📊 SQL-Trap-Eval: Frontier Model Leaderboard

> **Empirical resilience evaluation of frontier and open-weights LLMs against adversarial SQL logic traps.**

This leaderboard benchmarks models across our core adversarial vectors (`TRAP-001` through `TRAP-005`), testing whether models fall for subtle SQL traps or correctly resolve them using the SQLite execution oracle.

| Rank | Model Name | Tier | Traps Passed / 5 | Adversarial Vulnerability Rate |
| :---: | :--- | :--- | :---: | :---: |
| **#1** | Claude 3.5 Sonnet (Simulated Benchmark) | Frontier | 3/5 | `40.0%` vulnerability |
| **#2** | GPT-4o (Simulated Benchmark) | Frontier | 2/5 | `60.0%` vulnerability |
| **#3** | DeepSeek-V3 (Simulated Benchmark) | Open-Weights | 2/5 | `60.0%` vulnerability |
| **#4** | Llama 3.1 8B (Simulated) | Open-Weights | 1/5 | `80.0%` vulnerability |

---
*Benchmark generated dynamically via `leaderboard_gen.py` against the `sql-trap-eval` test harness.*
