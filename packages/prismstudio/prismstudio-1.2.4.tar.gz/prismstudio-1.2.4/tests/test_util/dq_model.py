from __future__ import annotations
from typing import Optional, List
from uuid import uuid4
import orjson
from pydantic import BaseModel, Field, UUID4, validator, root_validator


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() if idx > 0 else word.lower() for idx, word in enumerate(string.split('_')))


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default, option=orjson.OPT_NON_STR_KEYS).decode()


class PrismBaseModel(BaseModel):

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps

    @root_validator(pre=True)
    def log_pre_validation(cls, values):
        return values


class PrismQuery(PrismBaseModel):
    nodeid: Optional[UUID4] = Field(default_factory=uuid4)
    component_type: str
    componentid: Optional[int]
    categoryid: Optional[int] = None
    component_name: Optional[str] = None
    component_category: Optional[str] = None
    component_args: Optional[dict] = {}
    children: Optional[List[PrismQuery]] = []

