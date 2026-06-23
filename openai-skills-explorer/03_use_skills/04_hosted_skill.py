"""
04_hosted_skill.py

Demonstrates using a hosted Skill with Azure AI Foundry.

If no hosted skill is configured, the script exits gracefully.
"""

from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import client, MODEL

# Update this after a hosted skill is available
HOSTED_SKILL_ID = ""


def main():

    print("=" * 60)
    print("HOSTED SKILL")
    print("=" * 60)

    if not HOSTED_SKILL_ID:
        print("\nHosted skill is not configured.")
        print("Upload a skill in Azure AI Foundry and update HOSTED_SKILL_ID.")
        return

    question = input("\nBusiness Question:\n> ")

    start = time.perf_counter()

    response = client.responses.create(
        model=MODEL,
        skill_id=HOSTED_SKILL_ID,
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

    print(f"Latency      : {latency:.0f} ms")


if __name__ == "__main__":
    main()