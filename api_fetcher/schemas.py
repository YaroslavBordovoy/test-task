from typing import Annotated

from annotated_types import Gt, MinLen, MaxLen
from pydantic import BaseModel


class PostSchema(BaseModel):
    user_id: Annotated[int, Gt(0)]
    title: Annotated[str, MinLen(1), MaxLen(127)]
    body: Annotated[str, MinLen(1), MaxLen(511)]
