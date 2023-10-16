"""Dataset model."""
from typing import List, Optional

from pydantic import BaseModel, Field

from odp.models.common.common_subtypes import Metadata
from odp.models.common.contact_info import Contact


class DatasetSpecAttribute(BaseModel):
    """Dataset spec attribute class"""

    description: Optional[str] = None
    name: str
    traits: List[str]


class DatasetSpecCitation(BaseModel):
    """Dataset spec citation class"""

    cite_as: str
    doi: str


class DatasetSpec(BaseModel):
    """Dataset spec class."""

    attributes: List[DatasetSpecAttribute]
    citation: Optional[DatasetSpecCitation]
    data_collection: Optional[str] = None
    documentation: List[str] = Field(default_factory=list)
    maintainer: Contact
    storage_class: str = None
    storage_controller: Optional[str] = None
    tags: List[str]


class Dataset(BaseModel):
    """Dataset class."""

    metadata: Metadata
    spec: DatasetSpec
