"""
02_skill_router.py

Uses Azure AI Foundry + OpenAI Responses API to select the
most appropriate skill for a user's question.

This script ONLY routes.

It does not load SKILL.md or execute the selected skill.
"""

from pathlib import Path
import sys
import time

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import client, MODEL


AVAILABLE_SKILLS = """
Available Skills

1. claims_analysis
Use for:
- insurance claims
- fraud detection
- reserves
- loss analysis
- policy review

2. executive_summary
Use for:
- summarize reports
- AI playbooks
- governance documents
- frameworks
- recommendations

3. insurance
Use for:
- insurance concepts
- underwriting
- premiums
- products
- general insurance questions

Rules

Return ONLY the skill name.

Valid responses:

claims_analysis
executive_summary
insurance

Do not explain your answer.
Do not use markdown.
Do not add punctuation.
"""


def print_metrics(response, latency_ms: float):

    usage = getattr(response, "usage", None)

    print("\n" + "=" * 60)
    print("ROUTER METRICS")
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
    print("AI SKILL ROUTER")
    print("=" * 60)

    question = input("\nAsk a business question:\n> ")

    start = time.perf_counter()

    response = client.responses.create(
        model=MODEL,
        instructions=AVAILABLE_SKILLS,
        input=question,
    )

    latency_ms = (time.perf_counter() - start) * 1000

    selected_skill = response.output_text.strip()

    print("\n" + "=" * 60)
    print("SELECTED SKILL")
    print("=" * 60)
    print(selected_skill)

    print_metrics(response, latency_ms)


if __name__ == "__main__":
    main()