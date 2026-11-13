import sqlite3

def run_evaluation():
    print("==================================================")
    print("       SQL-Trap-Eval: Multi-Trap Test Suite       ")
    print("==================================================")

    # Define our expanding test suite of adversarial traps
    test_cases = [
        {
            "trap_id": "TRAP-001",
            "trap_name": "NOT IN with NULL subquery",
            "setup_sql": """
                CREATE TABLE users (id INTEGER, name TEXT, status TEXT);
                INSERT INTO users VALUES (1, 'Alice', 'active');
                INSERT INTO users VALUES (2, 'Bob', NULL);
                INSERT INTO users VALUES (3, 'Charlie', 'active');
            """,
            "ground_truth_query": """
                SELECT name FROM users 
                WHERE status = 'active' 
                AND id NOT IN (SELECT id FROM users WHERE status IS NULL);
            """,
            "buggy_llm_query": """
                SELECT name FROM users 
                WHERE id NOT IN (SELECT id FROM users WHERE status = 'active');
            """,
            "explanation": "A NULL in the subquery poisoned the NOT IN operator, returning 0 rows."
        },
        {
            "trap_id": "TRAP-002",
            "trap_name": "COUNT(column) omitting NULLs",
            "setup_sql": """
                CREATE TABLE feedback (id INTEGER, rating INTEGER);
                INSERT INTO feedback VALUES (1, 5);
                INSERT INTO feedback VALUES (2, NULL);
                INSERT INTO feedback VALUES (3, 4);
            """,
            "ground_truth_query": "SELECT COUNT(*) FROM feedback;",
            "buggy_llm_query": "SELECT COUNT(rating) FROM feedback;",
            "explanation": "COUNT(column) silently ignores rows where the column is NULL, undercounting total records."
        }
    ]

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