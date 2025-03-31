from typing import Literal, TypedDict

from pydantic import BaseModel

import cross.models

type API_TYPES = Literal[
    "SPACE",
    "POLYANET",
    "LEFT_COMETH",
    "RIGHT_COMETH",
    "UP_COMETH",
    "DOWN_COMETH",
    "PURPLE_SOLOON",
    "WHITE_SOLOON",
    "BLUE_SOLOON",
    "RED_SOLOON",
]


class UpdateMapRequest(TypedDict, total=False):
    row: str
    column: str
    candidateId: str


class GoalMapResponse(BaseModel):
    goal: list[list[API_TYPES]]
