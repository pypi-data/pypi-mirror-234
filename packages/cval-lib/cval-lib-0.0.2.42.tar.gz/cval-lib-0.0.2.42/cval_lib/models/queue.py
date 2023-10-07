from typing import Optional, List

from pydantic import BaseModel

from cval_lib.models._base import fields


@fields(
    'name: str',
    'capacity: int',
)
class QueueTask(BaseModel):
    name: str
    capacity: int


@fields(
    'capacity: int',
    'busy: int',
    'free: int',
    'usage: List[QueueTask]',
)
class QueueInfo(BaseModel):
    capacity: int
    busy: int
    free: int

    usage: List[QueueTask]
    in_queue: Optional[List[QueueTask]]
