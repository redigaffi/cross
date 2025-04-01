import pytest
import respx
from httpx import Response

from cross.app import main
from cross.config import Config

BASE_URL = Config().BASE_URL
CANDIDATE_ID = "test_candidate_id"


@pytest.mark.asyncio
@respx.mock
async def test_app(client):
    goal_map_response = {
        "goal": [["SPACE", "POLYANET"], ["PURPLE_SOLOON", "UP_COMETH"]]
    }
    get_map_route = respx.get(f"{BASE_URL}/map/{CANDIDATE_ID}/goal").mock(
        return_value=Response(200, json=goal_map_response)
    )

    update_polyanet_map_route = respx.post(f"{BASE_URL}/polyanets").mock(
        return_value=Response(200)
    )

    update_soloons_map_route = respx.post(f"{BASE_URL}/soloons").mock(
        return_value=Response(200)
    )

    update_cometh_map_route = respx.post(f"{BASE_URL}/comeths").mock(
        return_value=Response(200)
    )

    await main(client, CANDIDATE_ID)

    assert get_map_route.called
    assert update_polyanet_map_route.called
    assert update_soloons_map_route.called
    assert update_cometh_map_route.called

    assert (
        update_polyanet_map_route.calls[0].request.content
        == b'{"row":"0","column":"1","candidateId":"test_candidate_id"}'
    )
    assert (
        update_soloons_map_route.calls[0].request.content
        == b'{"row":"1","column":"0","candidateId":"test_candidate_id","color":"purple"}'
    )
    assert (
        update_cometh_map_route.calls[0].request.content
        == b'{"row":"1","column":"1","candidateId":"test_candidate_id","direction":"up"}'
    )
