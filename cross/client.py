import asyncio
from datetime import timedelta
from typing import Literal

import httpx
from httpx import Headers, HTTPStatusError
from tenacity import (RetryCallState, retry, stop_after_attempt,
                      wait_exponential)

from cross.cache import cache
from cross.models import GoalMapResponse, UpdateMapRequest
from cross.models.cometh import UpdateComethMapRequest
from cross.models.soloon import UpdateSoloonsMapRequest


async def handle_rate_limit(retry_state: RetryCallState) -> None:
    exception: HTTPStatusError = retry_state.outcome.exception()
    headers: Headers = exception.response.headers
    if exception.response.status_code == httpx.codes.TOO_MANY_REQUESTS:
        retry_after = int(headers.get("Retry-After") or 1)
        await asyncio.sleep(retry_after)

    await asyncio.sleep(1)


class CrossmintClient:
    def __init__(self, base_url: str):
        self._client = httpx.AsyncClient()
        self.base_url = base_url

    @retry(
        reraise=True,
        before_sleep=handle_rate_limit,
        wait=wait_exponential(multiplier=1, min=1, max=10),
        stop=stop_after_attempt(5),
    )
    @cache(ttl=timedelta(seconds=30), key="candidate_id:{candidate_id}")
    async def get_map(self, candidate_id: str) -> GoalMapResponse:
        """
        Retrieves the goal map for the given candidate ID.
        Request is retried up to 5 times with exponential backoff.
        Response is cached for 30 seconds.

        :param candidate_id: The candidate ID to retrieve the goal map for.
        :return: A GoalMapResponse object containing the goal map.
        :raises HTTPStatusError: If the request fails.
        """

        response = await self._client.get(f"{self.base_url}/map/{candidate_id}/goal")
        response.raise_for_status()
        json = response.content.decode("utf-8")
        return GoalMapResponse.model_validate_json(json)

    async def update_polyanet(self, req: UpdateMapRequest) -> None:
        """
        Updates the polyanet map with the given request data.

        :param req: An UpdateMapRequest object containing the update data.
        :raises HTTPStatusError: If the request fails.
        """

        await self.update_challenge_map("polyanets", req)

    async def update_soloons(self, req: UpdateSoloonsMapRequest) -> None:
        """
        Updates the soloons map with the given request data.

        :param req: An UpdateSoloonsMapRequest object containing the update data.
        :raises HTTPStatusError: If the request fails.
        """

        await self.update_challenge_map("soloons", req)

    async def update_cometh(self, req: UpdateComethMapRequest) -> None:
        """
        Updates the cometh map with the given request data.

        :param req: An UpdateComethMapRequest object containing the update data.
        :raises HTTPStatusError: If the request fails.
        """

        await self.update_challenge_map("comeths", req)

    @retry(
        reraise=True,
        before_sleep=handle_rate_limit,
        wait=wait_exponential(multiplier=1, min=1, max=10),
        stop=stop_after_attempt(5),
    )
    async def update_challenge_map(
        self,
        path: Literal["polyanets", "soloons", "comeths"],
        req: UpdateMapRequest | UpdateSoloonsMapRequest | UpdateComethMapRequest,
    ) -> None:
        """
        Updates the challenge map for the specified path with the given request data.
        Request is retried up to 5 times with exponential backoff.

        :param path: The path to update (polyanets, soloons, or comeths).
        :param req: An UpdateMapRequest, UpdateSoloonsMapRequest, or UpdateComethMapRequest object containing the update data.
        :raises HTTPStatusError: If the request fails.
        """

        response = await self._client.post(f"{self.base_url}/{path}", json=req)
        response.raise_for_status()

    def __del__(self):
        if not self._client.is_closed:
            asyncio.new_event_loop().run_until_complete(self._client.aclose())
