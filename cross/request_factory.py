from typing import Awaitable, Callable

from cross.client import CrossmintClient
from cross.models import UpdateMapRequest


def request_factory(
    crossmint_client: CrossmintClient, type
) -> Callable[[UpdateMapRequest], Awaitable[None]]:
    type = type.lower()
    if "_" in type:
        parameter, type_ = type.lower().split("_")
        if type_ == "cometh":
            return lambda data: crossmint_client.update_cometh(
                data | {"direction": parameter}
            )
        elif type_ == "soloon":
            return lambda data: crossmint_client.update_soloons(
                data | {"color": parameter}
            )

    elif type == "polyanet":
        return lambda data: crossmint_client.update_polyanet(data)
    elif type == "space":
        # Avoid the consumer of this API to handle a None situation (compared to returning None here),
        # so this API is more consistent, less error-prone, and better devx
        async def noop(data):
            pass

        return lambda data: noop(data)

    raise ValueError(f"Unknown API type: {type}")
