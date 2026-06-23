"""
01_basic_response.py

Purpose:
---------
Simple Azure AI Foundry + OpenAI Responses API example.

No SKILL.md.
No routing.
No helper classes.

This file verifies:

- Azure AI Foundry connection
- Responses API
- GPT model deployment
- response.output_text
- response.usage metrics
"""

from pathlib import Path
import sys
import time

# Allow importing config.py from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import client, MODEL


def print_metrics(response, latency_ms: float) -> None:
    """Print real metrics returned by the Responses API."""

    usage = getattr(response, "usage", None)

    print("\n" + "=" * 60)
    print("METRICS")
    print("=" * 60)

    if usage:
        print(f"Input Tokens : {getattr(usage, 'input_tokens', 'N/A')}")
        print(f"Output Tokens: {getattr(usage, 'output_tokens', 'N/A')}")
        print(f"Total Tokens : {getattr(usage, 'total_tokens', 'N/A')}")
    else:
        print("Input Tokens : N/A")
        print("Output Tokens: N/A")
        print("Total Tokens : N/A")

    print(f"Latency      : {latency_ms:.0f} ms")


def main():

    print("\n" + "=" * 60)
    print("AZURE AI FOUNDRY - BASIC RESPONSE")
    print("=" * 60)

    print("\nAsk anything:\n")

    user_question = input("> ").strip()

    if not user_question:
        print("No question provided.")
        return

    start = time.perf_counter()

    response = client.responses.create(
        model=MODEL,
        input=user_question,
    )

    latency_ms = (time.perf_counter() - start) * 1000

    print("\n" + "=" * 60)
    print("RESPONSE")
    print("=" * 60)
    print()

    print(response.output_text)

    print_metrics(response, latency_ms)


if __name__ == "__main__":
    main()