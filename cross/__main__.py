import asyncio

from cross.app import main
from cross.client import CrossmintClient
from cross.config import Config

config = Config()
CANDIDATE_ID: str = "5c2dcd74-79f0-488c-b1db-261617b09825"
crossmint_client = CrossmintClient(config.BASE_URL)

if __name__ == "__main__":
    asyncio.run(main(crossmint_client, CANDIDATE_ID))
