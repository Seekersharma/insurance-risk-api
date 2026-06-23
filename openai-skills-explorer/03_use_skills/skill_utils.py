"""
Utility functions for Azure OpenAI Responses API demonstrations.

Uses only REAL metrics from the API:
- response.usage.input_tokens
- response.usage.output_tokens
- response.usage.total_tokens
- time.perf_counter() for latency
"""

import logging
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import client, MODEL

logger = logging.getLogger(__name__)


@dataclass
class ApiResponse:
    text: str
    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None
    latency_ms: float


def load_skill_from_file(file_path: str | Path) -> str:
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Skill file not found: {file_path}")
    return file_path.read_text(encoding="utf-8")


def load_skill_from_github(github_url: str) -> str:
    if not github_url.startswith("https://"):
        raise ValueError("GitHub URL must use HTTPS")
    try:
        with urlopen(github_url, timeout=10) as response:
            return response.read().decode("utf-8")
    except URLError as exc:
        raise RuntimeError(f"Failed to download skill from GitHub: {exc}") from exc


def load_pdf_text(file_path: str | Path) -> str:
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    try:
        import PyPDF2
    except ImportError:
        logger.warning("PyPDF2 is not installed. PDF text extraction is disabled.")
        return ""

    text_pages: list[str] = []
    with file_path.open("rb") as file_obj:
        reader = PyPDF2.PdfReader(file_obj)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text:
                text_pages.append(page_text)

    return "\n\n".join(text_pages)


def _extract_response_text(response: object) -> str:
    text = getattr(response, "output_text", None)
    if text:
        return text

    outputs = getattr(response, "output", None)
    if isinstance(outputs, list) and outputs:
        first = outputs[0]
        content = getattr(first, "content", None)
        if isinstance(content, list) and content:
            first_content = content[0]
            return getattr(first_content, "text", "") or ""
    return ""


def call_responses_api(instructions: str, user_input: str) -> ApiResponse:
    start = time.perf_counter()

    response = client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=user_input,
    )

    latency_ms = (time.perf_counter() - start) * 1000
    usage = getattr(response, "usage", None)

    input_tokens = getattr(usage, "input_tokens", None) if usage else None
    output_tokens = getattr(usage, "output_tokens", None) if usage else None
    total_tokens = getattr(usage, "total_tokens", None) if usage else None

    return ApiResponse(
        text=_extract_response_text(response),
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        latency_ms=latency_ms,
    )


def setup_logging(name: str) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def format_metrics(response: ApiResponse) -> str:
    input_str = str(response.input_tokens) if response.input_tokens is not None else "N/A"
    output_str = str(response.output_tokens) if response.output_tokens is not None else "N/A"
    total_str = str(response.total_tokens) if response.total_tokens is not None else "N/A"
    return (
        f"Input Tokens: {input_str}\n"
        f"Output Tokens: {output_str}\n"
        f"Total Tokens: {total_str}\n"
        f"Latency: {response.latency_ms:.0f}ms"
    )
