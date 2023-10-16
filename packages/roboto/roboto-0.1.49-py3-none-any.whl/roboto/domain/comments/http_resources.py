import pydantic

from .record import EntityType


class CreateCommentRequest(pydantic.BaseModel):
    entity_type: EntityType
    entity_id: str
    comment_text: str


class UpdateCommentRequest(pydantic.BaseModel):
    comment_text: str
