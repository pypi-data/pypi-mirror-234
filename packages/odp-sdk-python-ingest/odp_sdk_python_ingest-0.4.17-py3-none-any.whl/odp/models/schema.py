"""Schema model."""
from typing import Dict, List, Literal

from pydantic import BaseModel


class ColumnType(BaseModel):
    """Column type class."""

    type: Literal["string", "double", "long", "geometry"]


class Schema(BaseModel):
    """Schema class."""

    table_description: str
    table_schema: Dict[str, ColumnType]
    geospatial_partition_columns: List[str]
    geospatial_partition_hash_precision: int = 5
    table_metadata: Dict[str, Dict[str, str]]
