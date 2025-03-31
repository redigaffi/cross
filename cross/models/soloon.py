from typing import Literal

from cross.models import UpdateMapRequest

type SUPPORTED_SOLOON_COLORS = Literal["purple", "white", "blue", "red"]


class UpdateSoloonsMapRequest(UpdateMapRequest):
    color: SUPPORTED_SOLOON_COLORS
