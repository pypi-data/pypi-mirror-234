from chimerapy.engine.networking import Server
from chimerapy.engine._logger import getLogger

logger = getLogger("chimerapy-engine")

if __name__ == "__main__":
    from pathlib import Path
    server = Server(
        id="server",
        host="localhost",
        port=5000,
        parent_logger=logger
    )
    server.tempfolder = Path(".")
    server.serve(blocking=True)
    while True:
        pass
