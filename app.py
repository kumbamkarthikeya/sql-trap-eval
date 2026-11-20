import os
import yaml
import sqlite3
from flask import Flask, render_template, request, jsonify
from eval_runner import evaluate_llm_live

app = Flask(__name__)

def load_traps():
    eval_path = os.path.join(os.path.dirname(__file__), 'eval.yml')
    print(f"Looking for eval.yml at: {eval_path}")
    if os.path.exists(eval_path):
        with open(eval_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if isinstance(data, dict):
                traps = data.get('traps', [])
            elif isinstance(data, list):
                traps = data
            else:
                traps = []
            print(f"Successfully loaded {len(traps)} traps.")
            return traps
    else:
        print("ERROR: eval.yml not found in directory!")
        return []

TRAPS = load_traps()

@app.route('/')
def index():
    return render_template('index.html', traps=TRAPS)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json() or {}
    trap_id = data.get('trap_id')
    mode = data.get('mode', 'llm')
    model_name = data.get('model')
    api_key = data.get('api_key')

    trap = next((t for t in TRAPS if t.get('trap_id') == trap_id), None)
    if not trap:
        return jsonify({"success": False, "error": "Trap not found"}), 404

    if mode == 'manual':
        user_query = (data.get('query') or '').strip()
        if not user_query:
            return jsonify({"success": False, "error": "Please enter a SQL query to test."})
        try:
            conn = sqlite3.connect(":memory:")
            cursor = conn.cursor()
            cursor.executescript(trap.get('setup_sql', ''))

            cursor.execute(trap.get('ground_truth_query', ''))
            expected_rows = cursor.fetchall()

            cursor.execute(user_query)
            actual_rows = cursor.fetchall()
            conn.close()

            passed = (actual_rows == expected_rows)
            return jsonify({
                "success": True,
                "passed": passed,
                "generated_sql": user_query,
                "expected": str(expected_rows),
                "actual": str(actual_rows),
                "message": "Query output matches ground truth." if passed else "Query output differs from ground truth."
            })
        except Exception as e:
            return jsonify({"success": False, "error": f"SQL Error: {e}"})

    result = evaluate_llm_live(trap, model_name, api_key)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)