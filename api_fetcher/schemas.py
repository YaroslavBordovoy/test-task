from typing import Annotated

from annotated_types import Gt, MinLen, MaxLen
from pydantic import BaseModel, ConfigDict, Field


class PostSchema(BaseModel):
    user_id: Annotated[int, Gt(0), Field(alias="userId")]
    title: Annotated[str, MinLen(1), MaxLen(127)]
    body: Annotated[str, MinLen(1), MaxLen(511)]

    model_config = ConfigDict(extra="ignore")
