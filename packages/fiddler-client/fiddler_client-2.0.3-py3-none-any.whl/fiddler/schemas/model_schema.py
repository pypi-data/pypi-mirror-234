from typing import List, Optional, Union

from pydantic import BaseModel

from fiddler.core_objects import DataType


class Column(BaseModel):
    """A model column representation"""

    name: str
    """Column name provided by the customer"""

    data_type: DataType
    """Data type of the column"""

    min: Optional[Union[int, float]] = None
    """Min value of integer/float column"""

    max: Optional[Union[int, float]] = None
    """Max value of integer/float column"""

    categories: Optional[List] = None
    """List of unique values of a categorical column"""

    bins: Optional[List[Union[int, float]]] = None
    """Bins of integer/float column"""

    replace_with_nulls: Optional[List] = None
    """Replace the list of given values to NULL if found in the events data"""

    n_dimensions: Optional[int] = None
    """Number of dimensions of a vector column"""

    class Config:
        smart_union = True


class ModelSchema(BaseModel):
    """Model schema with the details of each column"""

    schema_version: int = 1
    """Schema version"""

    columns: List[Column]
    """List of columns"""
