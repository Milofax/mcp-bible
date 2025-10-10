"""
Shared models and utilities for Bible MCP server
"""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response model"""
    error: str
    detail: str | None = None