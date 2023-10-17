from typing import Dict

from pydantic import BaseModel
from pydantic import conlist


class Rules(BaseModel):
    important_keys: Dict[str, type(str) | type(int)]
    hierarchy: conlist(str, min_length=1)

    class Config:
        json_schema_extra = dict(
            example=dict(
                important_keys=dict(
                    id=int,
                    name=str,
                    food=str,
                    type=str,
                ),
                hierarchy=["A", "B", "C"],
            )
        )
