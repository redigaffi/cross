import pytest
import respx
from httpx import Response

from cross.config import Config
from cross.models import GoalMapResponse, UpdateMapRequest
from cross.models.cometh import UpdateComethMapRequest
from cross.models.soloon import UpdateSoloonsMapRequest

BASE_URL = Config().BASE_URL
CANDIDATE_ID = "test_candidate_id_"



@pytest.mark.asyncio
@respx.mock
async def test_get_map(client):
    goal_map_response = {
        "goal": [["SPACE", "POLYANET"], ["LEFT_COMETH", "RIGHT_COMETH"]]
    }
    route = respx.get(f"{BASE_URL}/map/{CANDIDATE_ID}/goal").mock(
        return_value=Response(200, json=goal_map_response)
    )

    response = await client.get_map(CANDIDATE_ID)
    assert response == GoalMapResponse(
        goal=[["SPACE", "POLYANET"], ["LEFT_COMETH", "RIGHT_COMETH"]]
    )
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_update_polyanet(client):
    req = UpdateMapRequest(row="0", column="0", candidateId=CANDIDATE_ID)
    route = respx.post(f"{BASE_URL}/polyanets").mock(return_value=Response(200))

    await client.update_polyanet(req)
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_update_soloons(client):
    req = UpdateSoloonsMapRequest(
        row="0", column="0", candidateId=CANDIDATE_ID, color="red"
    )
    route = respx.post(f"{BASE_URL}/soloons").mock(return_value=Response(200))

    await client.update_soloons(req)
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_update_cometh(client):
    req = UpdateComethMapRequest(
        row="0", column="0", candidateId=CANDIDATE_ID, direction="up"
    )
    route = respx.post(f"{BASE_URL}/comeths").mock(return_value=Response(200))

    await client.update_cometh(req)
    assert route.called


@pytest.mark.asyncio
@respx.mock
async def test_update_challenge_map(client):
    req = UpdateMapRequest(row="0", column="0", candidateId=CANDIDATE_ID)
    route = respx.post(f"{BASE_URL}/polyanets").mock(return_value=Response(200))
    await client.update_challenge_map("polyanets", req)
    assert route.called
