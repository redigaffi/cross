import asyncio

from cross.app import main
from cross.client import CrossmintClient
from cross.config import Config

config = Config()
crossmint_client = CrossmintClient(config.BASE_URL)

if __name__ == "__main__":
    asyncio.run(main(crossmint_client, config.CANDIDATE_ID))
