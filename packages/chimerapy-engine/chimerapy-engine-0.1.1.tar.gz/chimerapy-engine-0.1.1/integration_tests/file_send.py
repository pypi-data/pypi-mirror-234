from chimerapy.engine.networking import Client
from chimerapy.engine._logger import getLogger
import asyncio
from pathlib import Path

logger = getLogger("chimerapy-engine")

if __name__ == "__main__":
    client = Client(
        id="client",
        host="localhost",
        port=5000,
        parent_logger=logger
    )
    asyncio.run(
        client.async_send_file(
            url="http://localhost:5000/file/post",
            sender_id="client",
            filepath=Path("../1GB.zip")
        )
    )
