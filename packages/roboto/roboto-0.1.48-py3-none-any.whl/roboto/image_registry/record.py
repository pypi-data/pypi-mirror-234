import pydantic


class ContainerImageRepositoryRecord(pydantic.BaseModel):
    org_id: str
    repository_name: str
    repository_uri: str
    arn: str


class ContainerImageRecord(pydantic.BaseModel):
    org_id: str
    repository_name: str
    image_tag: str
    image_uri: str
