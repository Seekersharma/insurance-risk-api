"""
Upload Skill using Multipart Form Data - Azure OpenAI Responses API.

Demonstrates how to create a skill by uploading individual files
using multipart form data encoding to Azure OpenAI.
"""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
from config import client

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def upload_skill_multipart(skill_dir: Path, skill_name: str) -> dict:
    """
    Upload a skill using multipart form data.
    
    Each skill file is uploaded as a separate form field. This approach
    allows more granular control over individual files compared to ZIP upload.
    
    Args:
        skill_dir: Path to skill directory containing SKILL.md
        skill_name: Name for the skill
        
    Returns:
        Response data from upload API
    """
    # Prepare files for multipart upload
    files = {}
    
    # Add SKILL.md as the primary skill definition
    skill_file = skill_dir / "SKILL.md"
    if skill_file.exists():
        with open(skill_file, "rb") as f:
            files["SKILL.md"] = ("SKILL.md", f.read(), "text/markdown")
        logger.info(f"Added SKILL.md ({skill_file.stat().st_size} bytes)")
    else:
        logger.error(f"SKILL.md not found: {skill_file}")
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")
    
    # Add supporting files
    for file_path in skill_dir.glob("*.md"):
        if file_path.name != "SKILL.md":
            with open(file_path, "rb") as f:
                mime_type = "text/markdown" if file_path.suffix == ".md" else "text/plain"
                files[file_path.name] = (file_path.name, f.read(), mime_type)
            logger.info(f"Added {file_path.name} ({file_path.stat().st_size} bytes)")
    
    # Add skill metadata as form field
    headers = {
        "api-key": client.api_key,
    }
    
    data = {
        "name": skill_name,
        "description": "Insurance claims analysis skill uploaded via multipart form data",
    }
    
    url = f"{client.base_url}/skills"
    
    logger.info(f"Uploading skill '{skill_name}' using multipart form data...")
    
    response = requests.post(url, headers=headers, data=data, files=files)
    
    if response.status_code in [200, 201]:
        logger.info(f"Upload successful: {response.status_code}")
        return response.json()
    else:
        logger.error(f"Upload failed: {response.status_code}")
        logger.error(f"Response: {response.text}")
        raise Exception(f"Upload failed with status {response.status_code}")


def main() -> None:
    """Run the multipart upload demonstration."""
    setup_logging(__name__)
    
    # Path to sample skill
    skill_dir = Path(__file__).resolve().parent.parent / "06_sample_skills" / "claims_analysis"
    
    if not skill_dir.exists():
        logger.error(f"Skill directory not found: {skill_dir}")
        return
    
    print("=" * 70)
    print("UPLOAD SKILL USING MULTIPART FORM DATA")
    print("=" * 70)
    print()
    
    try:
        # List files to upload
        logger.info(f"Skill directory: {skill_dir}")
        md_files = list(skill_dir.glob("*.md"))
        logger.info(f"Found {len(md_files)} markdown files to upload")
        
        # Upload skill
        skill_name = "claims-analysis-multipart-demo"
        result = upload_skill_multipart(skill_dir, skill_name)
        
        print("\n### UPLOAD RESULT ###\n")
        print(f"Skill Name: {result.get('name', 'N/A')}")
        print(f"Skill ID: {result.get('id', 'N/A')}")
        print(f"Version: {result.get('version', 'N/A')}")
        print(f"Status: {result.get('status', 'N/A')}")
        
        if "created_at" in result:
            print(f"Created: {result['created_at']}")
        
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
