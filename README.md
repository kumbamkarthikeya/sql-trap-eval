# SQL-Trap-Eval 🛡️⚡
> **Adversarial SQL Trap Evaluation Engine & Full-Stack Benchmark Dashboard**

[![SQL-Trap-Eval CI](https://github.com/Karthikeya-kumba/sql-trap-eval/actions/workflows/eval.yml/badge.svg)](https://github.com/Karthikeya-kumba/sql-trap-eval/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Overview
**SQL-Trap-Eval** is a high-precision adversarial evaluation harness designed to systematically test, catch, and benchmark LLM failure modes in complex SQL generation (such as `NOT IN` NULL poisoning, implicit cross-joins, aggregate filtering traps, and `COUNT()` omissions). 

Built to solve the core engineering challenge of **deterministic verification of stochastic AI outputs**, this platform features an in-memory SQLite oracle, a full-stack Tailwind CSS interactive query sandbox, automated CLI benchmark runners, and robust CI/CD pipelines.

---

## 🏗️ System Architecture & Core Components