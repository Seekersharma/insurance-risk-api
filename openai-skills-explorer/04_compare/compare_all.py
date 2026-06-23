"""
04_compare/compare_all.py

Compare different ways of using Azure AI Foundry +
OpenAI Responses API using REAL metrics only.
"""

import json
import time
from pathlib import Path
import sys

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import client, MODEL

PROJECT_ROOT = Path(__file__).resolve().parent.parent
METRICS_FILE = PROJECT_ROOT / "05_metrics" / "metrics_data.json"

LOCAL_SKILL = (
    PROJECT_ROOT
    / "06_sample_skills"
    / "claims_analysis"
    / "SKILL.md"
)

GITHUB_SKILL_URL = ""
HOSTED_SKILL_ID = ""

QUESTION = """
Analyze the following insurance claim and identify risk factors,
fraud indicators and recommended next steps.

Claim Amount: $15,500
Type: Auto Collision
Police Report: Yes
Days to Report: 2
"""


def run_response(method: str, instructions: str | None):

    start = time.perf_counter()

    if instructions:
        response = client.responses.create(
            model=MODEL,
            instructions=instructions,
            input=QUESTION,
        )
    else:
        response = client.responses.create(
            model=MODEL,
            input=QUESTION,
        )

    latency = (time.perf_counter() - start) * 1000

    usage = getattr(response, "usage", None)

    return {
        "method": method,
        "input_tokens": getattr(usage, "input_tokens", None) if usage else None,
        "output_tokens": getattr(usage, "output_tokens", None) if usage else None,
        "total_tokens": getattr(usage, "total_tokens", None) if usage else None,
        "latency": round(latency),
    }


def print_results(results):

    print("\n" + "=" * 85)
    print("AZURE AI FOUNDRY + OPENAI RESPONSES API COMPARISON")
    print("=" * 85)

    print(
        f'{"Method":<25}'
        f'{"Input":>12}'
        f'{"Output":>12}'
        f'{"Total":>12}'
        f'{"Latency(ms)":>15}'
    )

    print("-" * 85)

    for r in results:

        print(
            f'{r["method"]:<25}'
            f'{str(r["input_tokens"]):>12}'
            f'{str(r["output_tokens"]):>12}'
            f'{str(r["total_tokens"]):>12}'
            f'{str(r["latency"]):>15}'
        )


def main():

    results = []

    # Basic Response

    results.append(
        run_response(
            "Basic Response",
            None,
        )
    )

    # Inline Skill

    inline_skill = """
You are an experienced insurance claims analyst.

Provide:

1. Claim Summary
2. Risk Level
3. Fraud Indicators
4. Recommendation
"""

    results.append(
        run_response(
            "Inline Skill",
            inline_skill,
        )
    )

    # Local Skill

    local_skill = LOCAL_SKILL.read_text(encoding="utf-8")

    results.append(
        run_response(
            "Local SKILL.md",
            local_skill,
        )
    )

    # GitHub Skill

    if GITHUB_SKILL_URL:

        skill = requests.get(GITHUB_SKILL_URL, timeout=30).text

        results.append(
            run_response(
                "GitHub SKILL.md",
                skill,
            )
        )

    else:

        results.append(
            {
                "method": "GitHub SKILL.md",
                "input_tokens": "N/A",
                "output_tokens": "N/A",
                "total_tokens": "N/A",
                "latency": "Not Configured",
            }
        )

    # Hosted Skill

    results.append(
        {
            "method": "Hosted Skill",
            "input_tokens": "N/A",
            "output_tokens": "N/A",
            "total_tokens": "N/A",
            "latency": "Not Configured",
        }
    )

    METRICS_FILE.write_text(json.dumps(results, indent=2))

    print_results(results)


if __name__ == "__main__":
    main()