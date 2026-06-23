"""
Inline Skill - Azure OpenAI Responses API demonstration.

Shows how to provide instructions directly (no file loading).
Uses REAL metrics only from API response.
"""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from skill_utils import call_responses_api, setup_logging, format_metrics

logger = logging.getLogger(__name__)


def main() -> None:
    setup_logging(__name__)
    
    instructions = """
You are an insurance claims analyst. Analyze insurance claims and provide:
1. Claim summary and risk level
2. Fraud indicators (if any)
3. Recommended next steps

Be concise and professional.
"""
    
    user_query = """
Claim: POL-2024-001
Amount: $15,500
Type: Auto Collision
Days to Report: 2
Police Report: Yes

Analyze this claim.
"""
    
    print("=" * 50)
    print("INLINE SKILL")
    print("=" * 50)
    print()
    
    try:
        response = call_responses_api(instructions, user_query)
        print(response.text)
        print()
        print(format_metrics(response))
    except Exception as e:
        logger.error(f"Failed: {e}")
        raise


if __name__ == "__main__":
    main()

