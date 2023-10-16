"""Data collection model."""
from datetime import datetime
from typing import List

from pydantic import AnyUrl, BaseModel

from odp.models.common.common_subtypes import License, Metadata
from odp.models.common.contact_info import Contact


class DataCollectionSpecDistribution(BaseModel):
    """Data collection spec distribution class."""

    published_by: Contact
    published_date: datetime
    website: AnyUrl
    license: License


class DataCollectionSpec(BaseModel):
    """Data collection spec."""

    distribution: DataCollectionSpecDistribution
    tags: List[str]


class DataCollection(BaseModel):
    """Data collection class."""

    metadata: Metadata
    spec: DataCollectionSpec
