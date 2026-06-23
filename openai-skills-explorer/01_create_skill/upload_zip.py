"""
Upload Skill as ZIP File - Azure OpenAI Responses API.

Demonstrates how to create a skill by uploading a ZIP archive containing
SKILL.md and supporting files to Azure OpenAI.
"""

import logging
import sys
import zipfile
from io import BytesIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
from config import client

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def create_skill_zip(skill_dir: Path) -> BytesIO:
    """
    Create a ZIP file containing skill files.
    
    Args:
        skill_dir: Path to skill directory containing SKILL.md
        
    Returns:
        BytesIO object containing ZIP file data
    """
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add SKILL.md
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists():
            zf.write(skill_file, arcname="SKILL.md")
            logger.info(f"Added {skill_file.name}")
        
        # Add supporting files (e.g., README.md, example.md)
        for file in skill_dir.glob("*.md"):
            if file.name != "SKILL.md":
                zf.write(file, arcname=file.name)
                logger.info(f"Added {file.name}")
    
    zip_buffer.seek(0)
    return zip_buffer


def upload_skill_as_zip(zip_data: BytesIO, skill_name: str) -> dict:
    """
    Upload a skill ZIP file to Azure OpenAI.
    
    Args:
        zip_data: BytesIO object containing ZIP file
        skill_name: Name for the skill
        
    Returns:
        Response data from upload API
    """
    # Use the OpenAI client with requests to upload the ZIP
    headers = {
        "api-key": client.api_key,
    }
    
    url = f"{client.base_url}/skills"
    
    files = {
        "file": ("skill.zip", zip_data, "application/zip"),
        "name": (None, skill_name),
    }
    
    logger.info(f"Uploading skill '{skill_name}' as ZIP...")
    
    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code in [200, 201]:
        logger.info(f"Upload successful: {response.status_code}")
        return response.json()
    else:
        logger.error(f"Upload failed: {response.status_code}")
        logger.error(f"Response: {response.text}")
        raise Exception(f"Upload failed with status {response.status_code}")


def main() -> None:
    """Run the ZIP upload demonstration."""
    setup_logging(__name__)
    
    # Path to sample skill
    skill_dir = Path(__file__).resolve().parent.parent / "06_sample_skills" / "claims_analysis"
    
    if not skill_dir.exists():
        logger.error(f"Skill directory not found: {skill_dir}")
        return
    
    print("=" * 70)
    print("UPLOAD SKILL AS ZIP FILE")
    print("=" * 70)
    print()
    
    try:
        # Create ZIP file
        logger.info(f"Creating ZIP from: {skill_dir}")
        zip_data = create_skill_zip(skill_dir)
        logger.info(f"ZIP created: {zip_data.getbuffer().nbytes} bytes")
        
        # Upload to Azure OpenAI
        skill_name = "claims-analysis-zip-demo"
        result = upload_skill_as_zip(zip_data, skill_name)
        
        print("\n### UPLOAD RESULT ###\n")
        print(f"Skill Name: {result.get('name', 'N/A')}")
        print(f"Skill ID: {result.get('id', 'N/A')}")
        print(f"Version: {result.get('version', 'N/A')}")
        print(f"Status: {result.get('status', 'N/A')}")
        
        if "error" in result:
            print(f"Error: {result['error']}")
        
    except Exception as e:
        logger.error(f"Failed to upload skill: {e}")
        print(f"\nError: {e}")


def setup_logging(name: str) -> None:
    """Configure logging for the module."""
    logger_instance = logging.getLogger(name)
    logger_instance.setLevel(logging.INFO)
    
    if not logger_instance.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger_instance.addHandler(handler)


if __name__ == "__main__":
    main()
