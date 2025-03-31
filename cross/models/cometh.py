from typing import Literal

from cross.models import UpdateMapRequest

type SUPPORTED_COMETH_DIRECTIONS = Literal["left", "right", "up", "down"]


class UpdateComethMapRequest(UpdateMapRequest):
    direction: SUPPORTED_COMETH_DIRECTIONS
