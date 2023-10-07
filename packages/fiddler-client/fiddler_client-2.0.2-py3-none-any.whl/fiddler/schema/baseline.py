from typing import Optional

from fiddler.schema.base import BaseDataSchema


class Baseline(BaseDataSchema):
    id: Optional[int] = None
    name: str
    project_name: Optional[str]
    organization_name: Optional[str]
    type: Optional[str]
    model_name: Optional[str]

    dataset_name: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    offset: Optional[int] = None
    window_size: Optional[int] = None

    run_async: bool = True
