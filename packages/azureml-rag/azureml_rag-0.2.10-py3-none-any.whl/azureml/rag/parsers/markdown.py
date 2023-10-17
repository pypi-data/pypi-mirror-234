# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Markdown Parsing"""
from pydantic import BaseModel
from typing import Optional


class MarkdownBlock(BaseModel):
    """Markdown Block"""

    header: Optional[str]
    content: str
    parent: Optional["MarkdownBlock"] = None

    @property
    def header_level(self) -> int:
        """Get the header level of the block"""
        if self.header is None:
            return 0
        return self.header.count("#", 0, self.header.find(' '))
