import sqlite3

def run_evaluation():
    print("==================================================")
    print("       SQL-Trap-Eval: Automated Test Harness      ")
    print("==================================================")

    # 1. Define Trap #001: The NOT IN NULL Trap
    trap_id = "TRAP-001"
    trap_name = "NOT IN with NULL subquery"
    
    setup_sql = """
        CREATE TABLE users (id INTEGER, name TEXT, status TEXT);
        INSERT INTO users VALUES (1, 'Alice', 'active');
        INSERT INTO users VALUES (2, 'Bob', NULL);
        INSERT INTO users VALUES (3, 'Charlie', 'active');
    """
    
    # The correct query that handles NULLs properly (using NOT EXISTS or LEFT JOIN)
    ground_truth_query = """
        SELECT name FROM users 
        WHERE status = 'active' 
        AND id NOT IN (SELECT id FROM users WHERE status IS NULL);
    """
    
    # The naive LLM query that walks straight into the NULL trap
    buggy_llm_query = """
        SELECT name FROM users 
        WHERE id NOT IN (SELECT id FROM users WHERE status = 'active');
    """

    # 2. Spin up the In-Memory SQLite Oracle
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create tables and seed data
    cursor.executescript(setup_sql)

    # 3. Get Ground Truth Results
    cursor.execute(ground_truth_query)
    expected_results = cursor.fetchall()

    # 4. Get Buggy LLM Results
    cursor.execute(buggy_llm_query)
    actual_results = cursor.fetchall()

    # 5. Compare and Report
    print(f"\n[Test Case] {trap_id}: {trap_name}")
    print(f"  - Ground Truth Output: {expected_results}")
    print(f"  - Buggy Model Output:  {actual_results}")

    if expected_results == actual_results:
        print("  - Result: PASS (Queries matched)")
    else:
        print("  - Result: FAIL (Silent semantic error detected!)")
        print("  - Reason: A NULL in the subquery poisoned the NOT IN operator.")

    print("==================================================")
    conn.close()

if __name__ == "__main__":
    run_evaluation()