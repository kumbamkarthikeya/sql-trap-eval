import os
from flask import Flask, render_template, request, jsonify
import sqlite3
import json

app = Flask(__name__)

def load_traps():
    with open("traps.json", "r") as f:
        return json.load(f)

@app.route("/")
def index():
    traps = load_traps()
    return render_template("index.html", traps=traps)

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.json
    trap_id = data.get("trap_id")
    custom_query = data.get("query")
    
    traps = load_traps()
    target_trap = next((t for t in traps if t["trap_id"] == trap_id), None)
    
    if not target_trap:
        return jsonify({"error": "Trap not found"}), 404

    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.executescript(target_trap["setup_sql"])
        
        # Get Ground Truth
        cursor.execute(target_trap["ground_truth_query"])
        expected = cursor.fetchall()
        
        # Execute User/Query
        cursor.execute(custom_query)
        actual = cursor.fetchall()
        passed = (expected == actual)
        
        conn.close()
        return jsonify({
            "success": True,
            "passed": passed,
            "expected": str(expected),
            "actual": str(actual),
            "explanation": target_trap["explanation"]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "explanation": target_trap["explanation"]
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)