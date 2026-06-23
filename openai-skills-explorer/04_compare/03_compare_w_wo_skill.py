"""
03_compare_w_wo_skill.py

Live comparison of

WITHOUT SKILL
vs
WITH SKILL

using Azure AI Foundry + OpenAI Responses API.
"""

from pathlib import Path
import sys
import time

from pypdf import PdfReader

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import client, MODEL

SKILL_FOLDER = (
    PROJECT_ROOT
    / "06_sample_skills"
    / "executive_summary"
)

PDF_FILE = (
    PROJECT_ROOT
    / "07_sample_data"
    / "AI_RMF_Playbook.pdf"
)


def load_pdf():

    reader = PdfReader(PDF_FILE)

    text = []

    for page in reader.pages[:10]:
        text.append(page.extract_text() or "")

    return "\n".join(text)


def run_without_skill(question, document):

    instructions = """
You are a Senior Executive Strategy Consultant specializing in
Artificial Intelligence Governance, Enterprise Risk Management,
and Digital Transformation.

Analyze the supplied business document and create a concise
leadership briefing.

Return:

1. Executive Summary
2. Key Findings
3. Governance Highlights
4. Business Risks
5. Recommendations
6. Action Items

Use markdown headings.
Use bullet points.
Use business language.
Keep responses concise.
Never invent information.
"""

    start = time.perf_counter()

    response = client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=f"""
Business Question

{question}

Document

{document[:12000]}
""",
    )

    latency = (time.perf_counter() - start) * 1000

    usage = response.usage

    return {
        "input": usage.input_tokens,
        "output": usage.output_tokens,
        "total": usage.total_tokens,
        "latency": latency,
    }


def run_with_skill(question, document):

    instructions = (
        SKILL_FOLDER / "SKILL.md"
    ).read_text(encoding="utf-8")

    example = (
        SKILL_FOLDER / "example.md"
    ).read_text(encoding="utf-8")

    start = time.perf_counter()

    response = client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=f"""
Business Question

{question}

Example

{example}

Document

{document[:12000]}
""",
    )

    latency = (time.perf_counter() - start) * 1000

    usage = response.usage

    return {
        "input": usage.input_tokens,
        "output": usage.output_tokens,
        "total": usage.total_tokens,
        "latency": latency,
    }


def improvement(without_value, with_value):

    return f"-{((without_value - with_value) / without_value * 100):.0f}%"


def main():

    print("\n" + "=" * 62)
    print("Enterprise AI Skills Demo")
    print("Azure AI Foundry + OpenAI Responses API")
    print("=" * 62)

    question = input(
        "\nBusiness Question:\n> "
    )

    document = load_pdf()

    print("\nRunning WITHOUT SKILL ...")
    without_skill = run_without_skill(question, document)

    print("✓ Complete")

    print("\nRunning WITH SKILL ...")
    with_skill = run_with_skill(question, document)

    print("✓ Complete")

    print("\n")

    print("=" * 62)
    print("WITH SKILL vs WITHOUT SKILL")
    print("=" * 62)
    print()

    print(
        f'{"":20}'
        f'{"Without":>12}'
        f'{"With":>12}'
        f'{"Improvement":>15}'
    )

    print("-" * 62)

    print(
        f'{"Input Tokens":20}'
        f'{without_skill["input"]:>12}'
        f'{with_skill["input"]:>12}'
        f'{improvement(without_skill["input"],with_skill["input"]):>15}'
    )

    print(
        f'{"Output Tokens":20}'
        f'{without_skill["output"]:>12}'
        f'{with_skill["output"]:>12}'
        f'{improvement(without_skill["output"],with_skill["output"]):>15}'
    )

    print(
        f'{"Total Tokens":20}'
        f'{without_skill["total"]:>12}'
        f'{with_skill["total"]:>12}'
        f'{improvement(without_skill["total"],with_skill["total"]):>15}'
    )

    print(
        f'{"Latency (sec)":20}'
        f'{without_skill["latency"]/1000:>12.1f}'
        f'{with_skill["latency"]/1000:>12.1f}'
        f'{improvement(without_skill["latency"],with_skill["latency"]):>15}'
    )

    print("\n" + "=" * 62)

    print(
        """
Business Value

✓ Business logic externalized into SKILL.md
✓ Reusable across multiple applications
✓ Easier maintenance and versioning
✓ Standardized AI responses
✓ Lower token consumption
✓ Lower latency
"""
    )


if __name__ == "__main__":
    main()