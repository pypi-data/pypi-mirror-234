from fiddler.schema.base import BaseDataSchema


class CustomMetric(BaseDataSchema):
    id: str
    name: str
    project_name: str
    organization_name: str
    name: str
    fql: str
