from dataclasses import dataclass
from datetime import datetime
from typing import Optional

__all__ = ["FileInfo"]


@dataclass
class FileInfo:
    """Simple type to hold basic file information"""

    name: str
    checksum: str
    last_updated: datetime
    mime_type: str
    ref: Optional[str] = None
    contents: Optional[bytes] = None
