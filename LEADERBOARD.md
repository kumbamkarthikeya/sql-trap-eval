# 📊 SQL-Trap-Eval: Frontier Model Leaderboard

> **Comparative resilience evaluation of frontier and open-weights LLMs against adversarial SQL logic traps.**

This leaderboard benchmarks various language models across our 5 core adversarial vectors (`TRAP-001` through `TRAP-005`). Lower resilience scores indicate higher susceptibility to subtle SQL anti-patterns.

| Rank | Model Name | Tier | Traps Passed / 5 | Adversarial Vulnerability Rate |
| :---: | :--- | :--- | :---: | :---: |
| **#1** | Claude 3.5 Sonnet (Anthropic) | Frontier | 3/5 | `40.0%` vulnerability |
| **#2** | GPT-4o (OpenAI) | Frontier | 2/5 | `60.0%` vulnerability |
| **#3** | DeepSeek-V3 | Open-Weights | 2/5 | `60.0%` vulnerability |
| **#4** | Llama 3.1 70B (Meta) | Open-Weights | 1/5 | `80.0%` vulnerability |
| **#5** | Standard Base LLM | Baseline | 0/5 | `100.0%` vulnerability |

---
*Benchmark generated automatically via `leaderboard_gen.py` against the `sql-trap-eval` test harness.*
