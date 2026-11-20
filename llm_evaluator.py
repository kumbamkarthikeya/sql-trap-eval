import re
import requests

def extract_schema_only(setup_sql: str) -> str:
    """Extracts only CREATE TABLE statements so the LLM sees the schema without seeing the test data."""
    statements = [s.strip() for s in setup_sql.split(";") if s.strip()]
    create_stmts = [s + ";" for s in statements if s.upper().startswith("CREATE TABLE")]
    return "\n".join(create_stmts) if create_stmts else setup_sql

def clean_sql_response(raw_text: str) -> str:
    """Strips markdown code fences and whitespace from LLM SQL output."""
    cleaned = re.sub(r"```(?:sql)?", "", raw_text, flags=re.IGNORECASE)
    cleaned = cleaned.replace("```", "").strip()
    return cleaned

def generate_sql_from_llm(provider: str, model: str, api_key: str, setup_sql: str, task_prompt: str) -> str:
    """Calls the selected LLM provider API and returns a raw SQLite query."""
    schema_only = extract_schema_only(setup_sql)
    system_prompt = (
        "You are an expert SQL engineer. Given a SQLite table schema and a user request, "
        "write a single valid SQLite query that accurately fulfills the request. "
        "Return ONLY the raw SQL query—no explanations, no markdown formatting."
    )
    user_prompt = f"SQLite Schema:\n{schema_only}\n\nRequest:\n{task_prompt}\n\nSQL Query:"

    if provider == "openai":
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model or "gpt-4o",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.0
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return clean_sql_response(resp.json()["choices"][0]["message"]["content"])

    elif provider == "anthropic":
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model or "claude-3-5-sonnet-20241022",
            "max_tokens": 512,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
            "temperature": 0.0
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return clean_sql_response(resp.json()["content"][0]["text"])

    elif provider == "gemini":
        target_model = model or "gemini-1.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        }
        payload = {
            "contents": [{
                "parts": [{"text": f"{system_prompt}\n\n{user_prompt}"}]
            }]
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        return clean_sql_response(resp.json()["candidates"][0]["content"]["parts"][0]["text"])

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")