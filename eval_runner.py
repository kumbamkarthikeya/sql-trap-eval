import json
import re
import sqlite3
import time
import urllib.error
import urllib.request


def _strip_sql_fences(sql_text):
    cleaned = (sql_text or "").strip()
    cleaned = re.sub(r"^```(?:sql)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def evaluate_llm_live(trap, model_name, api_key):
    try:
        model = (model_name or "gemini-3.5-flash-lite").strip()
        if not api_key or not api_key.strip():
            return {"success": False, "error": "API key is missing."}

        prompt = (
            "You are a SQL benchmark test subject. Write a single SQL query "
            "to answer the requirement using the schema and sample data below.\n"
            f"Requirement: {trap.get('explanation', '')}\n"
            f"Schema/Setup SQL:\n{trap.get('setup_sql', '')}\n"
            "Return only the SQL query with no explanation."
        )

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent?key={api_key.strip()}"
        )

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        max_attempts = 3
        body = None

        for attempt in range(1, max_attempts + 1):
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=90) as resp:
                    body = json.loads(resp.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="replace")
                if e.code == 429:
                    return {
                        "success": False,
                        "error": (
                            f"Quota limit reached (HTTP 429) for model '{model}'. "
                            "Try switching to 'gemini-3.5-flash-lite' or 'gemini-3.1-flash-lite' "
                            "or wait for the daily quota reset."
                        ),
                    }
                if e.code == 503 and attempt < max_attempts:
                    time.sleep(1)
                    continue
                return {"success": False, "error": f"HTTP {e.code}: {err_body}"}

        candidates = (body or {}).get("candidates", [])
        parts = (
            candidates[0]
            .get("content", {})
            .get("parts", [])
            if candidates
            else []
        )
        raw_sql = "".join(p.get("text", "") for p in parts).strip()
        generated_sql = _strip_sql_fences(raw_sql)

        conn = sqlite3.connect(":memory:")
        try:
            cursor = conn.cursor()
            cursor.executescript(trap.get("setup_sql", ""))

            cursor.execute(trap.get("ground_truth_query", ""))
            expected_rows = cursor.fetchall()

            cursor.execute(generated_sql)
            actual_rows = cursor.fetchall()
        finally:
            conn.close()

        passed = actual_rows == expected_rows

        return {
            "success": True,
            "passed": passed,
            "generated_sql": generated_sql,
            "expected": str(expected_rows),
            "actual": str(actual_rows),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}