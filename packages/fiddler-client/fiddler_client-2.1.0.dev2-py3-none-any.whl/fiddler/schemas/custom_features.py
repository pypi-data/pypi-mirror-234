from enum import Enum
from typing import Any, Dict, List, Optional, Type, TypeVar

from pydantic import BaseModel

CustomFeatureTypeVar = TypeVar('CustomFeatureTypeVar', bound='CustomFeature')
DEFAULT_NUM_CLUSTERS = 5
DEFAULT_NUM_TAGS = 5


class CustomFeatureType(str, Enum):
    FROM_COLUMNS = 'FROM_COLUMNS'
    FROM_VECTOR = 'FROM_VECTOR'
    FROM_TEXT_EMBEDDING = 'FROM_TEXT_EMBEDDING'
    FROM_IMAGE_EMBEDDING = 'FROM_IMAGE_EMBEDDING'


class CustomFeature(BaseModel):
    name: str
    type: CustomFeatureType
    n_clusters: Optional[int] = DEFAULT_NUM_CLUSTERS
    centroids: Optional[List] = None
    columns: Optional[List[str]] = None
    column: Optional[str] = None
    source_column: Optional[str] = None
    n_tags: Optional[int] = DEFAULT_NUM_TAGS

    class Config:
        allow_mutation = False

    @classmethod
    def from_columns(
        cls, custom_name: str, cols: List[str], n_clusters: int = DEFAULT_NUM_CLUSTERS
    ) -> 'Multivariate':
        return Multivariate(
            name=custom_name,
            columns=cols,
            n_clusters=n_clusters,
        )

    @classmethod
    def from_dict(cls: Type[CustomFeatureTypeVar], deserialized_json: dict) -> Any:
        feature_type = CustomFeatureType(deserialized_json['type'])
        if feature_type == CustomFeatureType.FROM_COLUMNS:
            return Multivariate.parse_obj(deserialized_json)
        elif feature_type == CustomFeatureType.FROM_VECTOR:
            return VectorFeature.parse_obj(deserialized_json)
        elif feature_type == CustomFeatureType.FROM_TEXT_EMBEDDING:
            return TextEmbedding.parse_obj(deserialized_json)
        elif feature_type == CustomFeatureType.FROM_IMAGE_EMBEDDING:
            return ImageEmbedding.parse_obj(deserialized_json)
        else:
            raise ValueError(f'Unsupported feature type: {feature_type}')

    def to_dict(self) -> Dict[str, Any]:
        return_dict = {
            'name': self.name,
            'type': self.type,
            'n_clusters': self.n_clusters,
        }
        if self.type == CustomFeatureType.FROM_COLUMNS:
            return_dict['columns'] = self.columns  # type: ignore
        elif self.type == CustomFeatureType.FROM_VECTOR:
            return_dict['column'] = self.column
        elif self.type in (
            CustomFeatureType.FROM_TEXT_EMBEDDING,
            CustomFeatureType.FROM_IMAGE_EMBEDDING,
        ):
            return_dict['source_column'] = self.source_column
            return_dict['column'] = self.column

            if self.type == CustomFeatureType.FROM_TEXT_EMBEDDING:
                return_dict['n_tags'] = self.n_tags
        else:
            raise ValueError(f'Unsupported feature type: {self.type}')

        return return_dict


class Multivariate(CustomFeature):
    type: CustomFeatureType = CustomFeatureType.FROM_COLUMNS
    columns: List[str]
    monitor_components: bool = False


class VectorFeature(CustomFeature):
    type: CustomFeatureType = CustomFeatureType.FROM_VECTOR
    source_column: Optional[str] = None
    column: str


class TextEmbedding(VectorFeature):
    type: CustomFeatureType = CustomFeatureType.FROM_TEXT_EMBEDDING
    n_tags: Optional[int] = DEFAULT_NUM_TAGS


class ImageEmbedding(VectorFeature):
    type: CustomFeatureType = CustomFeatureType.FROM_IMAGE_EMBEDDING
