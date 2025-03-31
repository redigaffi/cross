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
    if exception.response.status_code == 429:
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
        response = await self._client.get(f"{self.base_url}/map/{candidate_id}/goal")
        response.raise_for_status()
        json = response.content.decode("utf-8")
        return GoalMapResponse.model_validate_json(json)

    async def update_polyanet(self, req: UpdateMapRequest) -> None:
        await self.update_challenge_map("polyanets", req)

    async def update_soloons(self, req: UpdateSoloonsMapRequest) -> None:
        await self.update_challenge_map("soloons", req)

    async def update_cometh(self, req: UpdateComethMapRequest) -> None:
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
        response = await self._client.post(f"{self.base_url}/{path}", json=req)
        response.raise_for_status()

    def __del__(self):
        if not self._client.is_closed:
            asyncio.new_event_loop().run_until_complete(self._client.aclose())
