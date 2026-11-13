import sqlite3
import json

def load_traps(filepath="traps.json"):
    """Loads adversarial SQL traps from an external JSON benchmark file."""
    with open(filepath, "r") as f:
        return json.load(f)

def run_evaluation():
    print("==================================================")
    print("       SQL-Trap-Eval: JSON-Driven Test Runner     ")
    print("==================================================")

    # Load test cases dynamically from our external benchmark file
    try:
        test_cases = load_traps("traps.json")
    except FileNotFoundError:
        print("Error: traps.json not found! Please check file placement.")
        return

    detected_traps = 0

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

        if expected == actual:
            print("  - Status: PASS")
        else:
            print("  - Status: FAIL (Silent semantic error caught!)")
            print(f"  - Reason: {test['explanation']}")
            detected_traps += 1

        conn.close()

    print("==================================================")
    print(f"Suite Summary: {detected_traps} / {len(test_cases)} Adversarial Traps Successfully Triggered")
    print("==================================================")

if __name__ == "__main__":
    run_evaluation()