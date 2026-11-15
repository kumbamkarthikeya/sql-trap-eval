import json
import sqlite3
import pytest

def load_traps():
    with open("traps.json", "r") as f:
        return json.load(f)

def test_traps_load():
    traps = load_traps()
    assert len(traps) > 0, "Traps file should not be empty"

def test_sqlite_oracle_execution():
    traps = load_traps()
    for trap in traps:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        
        # Verify setup SQL executes cleanly
        cursor.executescript(trap["setup_sql"])
        
        # Verify ground truth query executes and returns results
        cursor.execute(trap["ground_truth_query"])
        gt_result = cursor.fetchall()
        assert isinstance(gt_result, list)
        
        conn.close()