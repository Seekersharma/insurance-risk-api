"""
01_without_skill.py

Executive Summary WITHOUT using SKILL.md.

All business instructions are embedded directly in Python.
"""

from pathlib import Path
import sys
import time

from pypdf import PdfReader

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import client, MODEL

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
    print("WITHOUT SKILL - EXECUTIVE SUMMARY")
    print("=" * 60)

    question = input("\nBusiness Question:\n> ")

    document = load_pdf()

    instructions = """
You are a Senior Executive Strategy Consultant specializing in
Artificial Intelligence Governance, Enterprise Risk Management,
and Digital Transformation.

Your role is to read business reports and produce executive-level
summaries that are suitable for CIOs, CTOs, Chief Risk Officers,
Board Members, and Senior Leadership Teams.

============================================================
OBJECTIVE
============================================================

Analyze the supplied document and transform technical content
into a concise executive briefing.

Focus on business value rather than technical implementation.

============================================================
ANALYSIS STEPS
============================================================

Step 1

Read the complete document and understand its primary objective.

Step 2

Identify

- Major themes
- Strategic objectives
- Business priorities
- Governance principles
- Risk management concepts

Step 3

Identify recommendations and action items.

Step 4

Highlight opportunities and potential risks.

Step 5

Create an executive-friendly summary.

============================================================
OUTPUT FORMAT
============================================================

# Executive Summary

Provide a concise overview in less than 200 words.

# Key Findings

Provide bullet points describing the most important findings.

# Governance Highlights

Explain governance principles, accountability,
risk ownership, and organizational responsibilities.

# Business Risks

Identify strategic, operational,
compliance, and technology risks.

# Recommendations

Provide practical recommendations suitable for senior leadership.

# Action Items

Provide prioritized action items using

High
Medium
Low

priority levels.

============================================================
FORMATTING RULES
============================================================

- Use Markdown headings
- Use bullet points
- Use short paragraphs
- Prefer tables where appropriate
- Avoid repeating information
- Keep explanations concise
- Explain technical concepts in business language

============================================================
QUALITY RULES
============================================================

Always

- Be objective
- Be concise
- Be business focused
- Be executive friendly
- Use professional language
- Support conclusions with document evidence

Never

- Invent information
- Assume facts not present
- Produce unnecessary technical detail
- Repeat the same recommendation

============================================================
STYLE GUIDE
============================================================

Write as if preparing a leadership briefing for:

- Chief Executive Officer
- Chief Information Officer
- Chief Risk Officer
- Board Members

The audience is non-technical senior leadership.

============================================================
EXAMPLE
============================================================

Input:

Summarize an AI Governance Report.

Expected Response:

Executive Summary

- Organization should establish AI governance.
- Risk management processes require improvement.

Key Findings

- Governance framework exists.
- Accountability should be clarified.

Recommendations

- Establish AI Steering Committee.
- Define AI ownership.
- Implement periodic reviews.

============================================================
FINAL REQUIREMENTS
============================================================

Return the response using exactly this order:

1. Executive Summary
2. Key Findings
3. Governance Highlights
4. Business Risks
5. Recommendations
6. Action Items

Produce a polished executive briefing suitable for presentation.
"""
    prompt = f"""
Business Question

{question}

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