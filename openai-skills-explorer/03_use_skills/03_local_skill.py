"""
03_local_skill.py

Execute a local SKILL.md using Azure AI Foundry Responses API.

Flow

skill_name
    ↓
load SKILL.md
    ↓
load config.json
    ↓
load configured sample data
    ↓
Azure OpenAI Responses API
    ↓
Answer + Real Metrics
"""

import json
import time
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import client, MODEL

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "06_sample_skills"
DATA_DIR = ROOT / "07_sample_data"


def load_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_pdf(path: Path) -> str:

    if PdfReader is None:
        return "PyPDF is not installed."

    reader = PdfReader(path)
    text = []

    for page in reader.pages[:10]:
        text.append(page.extract_text() or "")

    return "\n".join(text)


def load_csv(path: Path) -> str:

    if pd is None:
        return path.read_text()

    df = pd.read_csv(path)

    return df.head(25).to_markdown(index=False)


def load_document(path: Path) -> str:

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return load_pdf(path)

    if suffix == ".csv":
        return load_csv(path)

    return load_text_file(path)


def print_metrics(response, latency):

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


def run_skill(skill_name: str, question: str):

    skill_folder = SKILLS_DIR / skill_name

    skill_md = skill_folder / "SKILL.md"
    config_json = skill_folder / "config.json"

    instructions = load_text_file(skill_md)

    config = json.loads(config_json.read_text())

    data_file = DATA_DIR / config["data_file"]

    document_text = load_document(data_file)

    prompt = f"""
Business Question

{question}

Business Document

{document_text[:12000]}
"""

    start = time.perf_counter()

    response = client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=prompt,
    )

    latency = (time.perf_counter() - start) * 1000

    print("\n" + "=" * 60)
    print(f"LOCAL SKILL : {skill_name}")
    print("=" * 60)

    print(f"\nData Source : {data_file.name}\n")

    print(response.output_text)

    print_metrics(response, latency)


def main():

    print("\nEnterprise AI Skills Explorer\n")

    skill = input("Skill name (claims_analysis/executive_summary/insurance): ")

    question = input("\nBusiness question:\n> ")

    run_skill(skill.strip(), question.strip())


if __name__ == "__main__":
    main()