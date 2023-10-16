from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import AnyUrl, BaseModel


class Metadata(BaseModel):
    name: str
    description: str
    display_name: str
    labels: Dict[str, Any]
    owner: Optional[UUID] = None
    uuid: Optional[UUID] = None


class License(BaseModel):
    name: str
    full_text: str
    href: AnyUrl
