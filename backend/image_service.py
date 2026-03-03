import os
import base64
import requests


def generate_image(final_event: str) -> str:
    """Generate an image for the final timeline event using Together.ai.
    Returns a base64 data URL string."""

    api_key = os.getenv("TOGETHER_API_KEY", "")
    if not api_key:
        raise ValueError("TOGETHER_API_KEY environment variable is not set.")

    prompt = (
        f"A cinematic, dramatic illustration of this life moment: {final_event}. "
        "Vibrant colors, epic atmosphere, digital art style."
    )

    response = requests.post(
        "https://api.together.xyz/v1/images/generations",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "black-forest-labs/FLUX.1-schnell-Free",
            "prompt": prompt,
            "width": 512,
            "height": 512,
            "n": 1,
            "response_format": "b64_json",
        },
        timeout=60,
    )

    if response.status_code != 200:
        raise ValueError(f"Together.ai API error: {response.status_code} {response.text[:200]}")

    data = response.json()
    b64 = data["data"][0]["b64_json"]
    return f"data:image/png;base64,{b64}"
