from fiddler.schema.base import BaseDataSchema


class Webhook(BaseDataSchema):
    uuid: str
    name: str
    organization_name: str
    url: str
    # provider is 'SLACK' or 'OTHER' as of Aug 2023.
    provider: str
