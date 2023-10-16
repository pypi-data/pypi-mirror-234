from typing import List

from pydantic import BaseModel

from fiddler.schemas.custom_features import CustomFeature


class ModelSpec(BaseModel):
    """Model spec defines how model columns are used along with model task"""

    schema_version: int = 1
    """Schema version"""

    inputs: List[str] = []
    """Feature columns"""

    outputs: List[str] = []
    """Prediction columns"""

    targets: List[str] = []
    """Label columns"""

    decisions: List[str] = []
    """Decisions columns"""

    metadata: List[str] = []
    """Metadata columns"""

    custom_features: List[CustomFeature] = []
    """Custom feature definitions"""
