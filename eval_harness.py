import sqlite3
import json
import datetime

def load_traps(filepath="traps.json"):
    """Loads adversarial SQL traps from an external JSON benchmark file."""
    with open(filepath, "r") as f:
        return json.load(f)

def run_evaluation():
    print("==================================================")
    print("    SQL-Trap-Eval: Benchmark Report & Runner      ")
    print("==================================================")

    try:
        test_cases = load_traps("traps.json")
    except FileNotFoundError:
        print("Error: traps.json not found! Please check file placement.")
        return

    detected_traps = 0
    report_results = []

    # Execute each test case through the in-memory SQLite oracle
    for test in test_cases:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        
        # Setup tables and data
        cursor.executescript(test["setup_sql"])
        
        # Get Ground Truth
        cursor.execute(test["ground_truth_query"])
        expected = cursor.fetchall()
        
        # Get LLM Buggy Output
        cursor.execute(test["buggy_llm_query"])
        actual = cursor.fetchall()

        print(f"\n[Test Case] {test['trap_id']}: {test['trap_name']}")
        print(f"  - Ground Truth: {expected}")
        print(f"  - LLM Output:   {actual}")

        passed = (expected == actual)
        if passed:
            print("  - Status: PASS")
            status = "PASS"
        else:
            print("  - Status: FAIL (Silent semantic error caught!)")
            print(f"  - Reason: {test['explanation']}")
            status = "FAIL"
            detected_traps += 1

        # Append result for JSON reporting
        report_results.append({
            "trap_id": test["trap_id"],
            "trap_name": test["trap_name"],
            "status": status,
            "ground_truth": str(expected),
            "llm_output": str(actual),
            "explanation": test["explanation"]
        })

        conn.close()

    # Generate structured benchmark report JSON
    report = {
        "timestamp": str(datetime.datetime.now()),
        "total_traps": len(test_cases),
        "traps_triggered": detected_traps,
        "results": report_results
    }

    with open("eval_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("\n==================================================")
    print(f"Suite Summary: {detected_traps} / {len(test_cases)} Adversarial Traps Successfully Triggered")
    print("Benchmark report successfully exported to eval_report.json")
    print("==================================================")

if __name__ == "__main__":
    run_evaluation()