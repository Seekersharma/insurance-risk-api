"""
05_github_skill.py

Load a SKILL.md from a GitHub raw URL and use it with
Azure AI Foundry + OpenAI Responses API.

Uses:
- GitHub hosted SKILL.md
- Real response.usage metrics
- Real latency
"""

from pathlib import Path
import sys
import time

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import client, MODEL

# Update with your own GitHub raw URL
GITHUB_SKILL_URL = ""


def load_skill(url: str) -> str:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def main():

    print("=" * 60)
    print("GITHUB SKILL")
    print("=" * 60)

    if not GITHUB_SKILL_URL:
        print("\nGitHub SKILL.md URL is not configured.")
        print("Update GITHUB_SKILL_URL with a raw GitHub URL.")
        return

    question = input("\nBusiness Question:\n> ")

    instructions = load_skill(GITHUB_SKILL_URL)

    start = time.perf_counter()

    response = client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=question,
    )

    latency = (time.perf_counter() - start) * 1000

    print("\nRESPONSE\n")
    print(response.output_text)

    usage = getattr(response, "usage", None)

    print("\n" + "=" * 60)
    print("METRICS")
    print("=" * 60)

    if usage:
        print(f"Input Tokens : {usage.input_tokens}")
        print(f"Output Tokens: {usage.output_tokens}")
        print(f"Total Tokens : {usage.total_tokens}")
    else:
        print("Input Tokens : N/A")
        print("Output Tokens: N/A")
        print("Total Tokens : N/A")

    print(f"Latency      : {latency:.0f} ms)


if __name__ == "__main__":
    main()