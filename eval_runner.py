import json
import sqlite3
import sys

def run_benchmark():
    print("🚀 Initializing SQL-Trap-Eval Automated Benchmark Runner...")
    
    try:
        with open("traps.json", "r") as f:
            traps = json.load(f)
    except FileNotFoundError:
        print("❌ Error: traps.json not found in root directory.")
        sys.exit(1)

    total_traps = len(traps)
    traps_caught = 0
    execution_results = []

    print(f"📊 Loaded {total_traps} adversarial SQL traps. Executing against SQLite oracle...\n")

    for trap in traps:
        trap_id = trap["trap_id"]
        trap_name = trap["trap_name"]
        setup_sql = trap["setup_sql"]
        gt_query = trap["ground_truth_query"]
        buggy_query = trap["buggy_llm_query"]

        try:
            conn = sqlite3.connect(":memory:")
            cursor = conn.cursor()
            cursor.executescript(setup_sql)

            # Get Ground Truth
            cursor.execute(gt_query)
            expected = cursor.fetchall()

            # Execute Buggy LLM Query
            cursor.execute(buggy_query)
            actual = cursor.fetchall()
            
            passed = (expected == actual)
            conn.close()

            # If passed is False, the adversarial trap successfully caught the LLM failure!
            caught = not passed
            if caught:
                traps_caught += 1

            status = "CAUGHT TRAP 🛡️" if caught else "PASSED (LLM beat trap) ⚠️"
            print(f"[{trap_id}] {trap_name}")
            print(f"  Status:   {status}")
            print(f"  Expected: {expected}")
            print(f"  Actual:   {actual}\n")

            execution_results.append({
                "trap_id": trap_id,
                "trap_name": trap_name,
                "caught_trap": caught,
                "expected": str(expected),
                "actual": str(actual)
            })

        except Exception as e:
            print(f"[{trap_id}] {trap_name}")
            print(f"  Status:   TRAP TRIGGERED (SQL Execution Error: {e}) 💥\n")
            traps_caught += 1  # SQL execution error means the trap successfully broke the query
            execution_results.append({
                "trap_id": trap_id,
                "trap_name": trap_name,
                "caught_trap": True,
                "error": str(e)
            })

    # Summary Scorecard
    scorecard = {
        "total_traps": total_traps,
        "traps_caught": traps_caught,
        "adversarial_catch_rate": f"{(traps_caught / total_traps) * 100:.1f}%"
    }

    print("=" * 50)
    print("📈 BENCHMARK SUMMARY SCORECARD")
    print(f"  Total Traps Evaluated:    {scorecard['total_traps']}")
    print(f"  Traps Successfully Caught: {scorecard['traps_caught']}")
    print(f"  Adversarial Catch Rate:   {scorecard['adversarial_catch_rate']}")
    print("=" * 50)

    # Save structured report
    report = {
        "benchmark": "sql-trap-eval",
        "scorecard": scorecard,
        "results": execution_results
    }
    
    with open("benchmark_results.json", "w") as out:
        json.dump(report, out, indent=2)
    print("💾 Quantitative benchmark report saved to 'benchmark_results.json'.")

if __name__ == "__main__":
    run_benchmark()