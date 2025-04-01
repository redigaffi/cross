from httpx import HTTPStatusError

from cross.client import CrossmintClient
from cross.logger import logger
from cross.models import API_TYPES, UpdateMapRequest
from cross.request_factory import request_factory


async def main(crossmint_client: CrossmintClient, candidate_id: str):
    """
    Main function to execute the Crossmint challenge

    :param crossmint_client:
    :param candidate_id:
    :return:
    """

    logger.info("Starting Crossmint challenge")
    map_ = await crossmint_client.get_map(candidate_id)

    for row_idx, row in enumerate(map_.goal):
        col: API_TYPES
        for col_idx, col in enumerate(row):
            data: UpdateMapRequest = {
                "row": str(row_idx),
                "column": str(col_idx),
                "candidateId": candidate_id,
            }

            execute_call = request_factory(crossmint_client, col)

            try:
                await execute_call(data)
            except HTTPStatusError as e:
                logger.error(f"Failed HTTP call to update {col} type", exc_info=e)
            except Exception as e:
                logger.critical(
                    f"Something unexpected happened updating {col} type", exc_info=e
                )

    logger.info("Finished Crossmint challenge")
