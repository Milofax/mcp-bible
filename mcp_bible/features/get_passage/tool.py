"""
MCP Tool: Get Bible Passage

Provides the get_passage tool for AI assistants.
"""

import logging
from typing import Dict, Any

from fastmcp import FastMCP

from mcp_bible.bible_service import BibleService
from mcp_bible.features.get_passage.models import GetPassageRequest, GetPassageResponse

logger = logging.getLogger(__name__)


def register_tool(mcp: FastMCP, bible_service: BibleService) -> None:
    """
    Register the get_passage tool with the MCP server

    Args:
        mcp: FastMCP server instance
        bible_service: BibleService instance for Bible operations
    """
    @mcp.tool()
    async def get_passage(passage: str, version: str = "ESV") -> Dict[str, Any]:
        """
        Get a Bible passage from BibleGateway.com

        This tool enables AI assistants to retrieve Bible passages for users.
        It supports multiple Bible translations and provides clean, formatted text.

        Use this tool when users ask questions like:
        - "Show me John 3:16"
        - "What does Romans 8 say?"
        - "Read Psalm 23 in NIV"
        - "Get the text of Genesis 1"

        Features:
        - Support for 8+ Bible translations
        - Automatic HTML parsing and cleaning
        - Error handling for invalid passages
        - Footnotes and cross-references removed

        Args:
            passage (str): Bible reference to retrieve
                Examples: "John 3:16", "Romans 8:28-30", "Psalm 23", "Genesis 1:1-10"

            version (str, optional): Bible translation version
                Default: "ESV" (English Standard Version)
                Supported: ESV, NIV, KJV, NASB, NKJV, NLT, AMP, MSG

        Returns:
            dict: Passage result containing:
                - success: Whether the request succeeded
                - passage: The requested reference
                - version: The Bible version used
                - text: The passage text (if successful)
                - error: Error message (if failed)

        Raises:
            ValueError: If passage reference is invalid or version is unsupported

        Example Usage (in AI conversation):
            User: "Show me John 3:16"

            AI calls: get_passage("John 3:16")

            AI responds: "Here's John 3:16 from the ESV: 'For God so loved the world, that he gave his only Son, that whoever believes in him should not perish but have eternal life.'"
        """
        try:
            logger.info(f"MCP tool called: get_passage(passage='{passage}', version='{version}')")

            # Create and validate request
            request = GetPassageRequest(
                passage=passage,
                version=version
            )

            # Call bible service
            result = await bible_service.fetch_passage(
                passage=request.passage,
                version=request.version
            )

            logger.info(f"Passage retrieval completed: {passage} ({version})")
            return result

        except ValueError as e:
            logger.warning(f"Passage validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Passage retrieval error: {e}")
            raise