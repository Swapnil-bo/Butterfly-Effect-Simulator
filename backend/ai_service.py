import re
import json
import os
from openai import OpenAI
from prompt_builder import SYSTEM_PROMPT, build_user_prompt

MAX_RETRIES = 3


def get_client():
    provider = os.getenv("LLM_PROVIDER", "ollama")
    if provider == "groq":
        return OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY"),
        )
    return OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def get_model() -> str:
    provider = os.getenv("LLM_PROVIDER", "ollama")
    if provider == "groq":
        return "llama3-8b-8192"
    return "qwen2.5:3b"


def extract_valid_json(raw_response: str) -> list:
    cleaned = re.sub(r"```(?:json)?|```", "", raw_response).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError("LLM failed to produce valid JSON after cleaning.")


def generate_timeline(user_decision: str) -> list:
    client = get_client()
    model = get_model()
    user_prompt = build_user_prompt(user_decision)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
            )
            raw = response.choices[0].message.content
            nodes = extract_valid_json(raw)

            if not isinstance(nodes, list) or not (5 <= len(nodes) <= 7):
                raise ValueError(f"Expected 5-7 nodes, got {len(nodes)}")

            return nodes

        except (ValueError, KeyError) as e:
            if attempt == MAX_RETRIES:
                raise ValueError(
                    f"Failed after {MAX_RETRIES} attempts. Last error: {e}"
                )

    raise ValueError("Unreachable: retry loop exited without return or raise.")
