"""
02_with_skill.py

Executive Summary WITH SKILL.md.

Business instructions are loaded from a reusable SKILL.md
instead of being embedded in Python.
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


def load_pdf() -> str:

    reader = PdfReader(PDF_FILE)

    text = []

    for page in reader.pages[:10]:
        text.append(page.extract_text() or "")

    return "\n".join(text)


def print_metrics(response, latency_ms):

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

    print(f"Latency      : {latency_ms:.0f} ms")


def main():

    print("=" * 60)
    print("WITH SKILL - EXECUTIVE SUMMARY")
    print("=" * 60)

    question = input("\nBusiness Question:\n> ")

    instructions = (
        SKILL_FOLDER / "SKILL.md"
    ).read_text(encoding="utf-8")

    example = ""

    example_file = SKILL_FOLDER / "example.md"

    if example_file.exists():
        example = example_file.read_text(encoding="utf-8")

    document = load_pdf()

    prompt = f"""
Business Question

{question}

Example

{example}

Document

{document[:12000]}
"""

    start = time.perf_counter()

    response = client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=prompt,
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