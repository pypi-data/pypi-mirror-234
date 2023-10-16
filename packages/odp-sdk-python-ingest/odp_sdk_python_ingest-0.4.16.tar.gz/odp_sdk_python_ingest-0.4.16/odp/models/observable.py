"""Observable model."""
from typing import Any

from pydantic import BaseModel

from odp.models.common.common_subtypes import Metadata, Spec


class ObservableDetails(BaseModel):
    """Observable details."""

    value: Any
    cls: str


class ObservableSpec(Spec):
    """Observable spec class."""

    ref: str
    details: ObservableDetails


class Observable(BaseModel):
    """Observable class."""

    metadata: Metadata
    spec: ObservableSpec
