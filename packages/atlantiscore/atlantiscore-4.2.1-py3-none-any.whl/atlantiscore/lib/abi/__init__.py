import json
from pathlib import Path

import aiofiles


async def read_abi(name: str) -> dict:
    path = Path(__file__).parent / f"{name}.abi"
    async with aiofiles.open(path, mode="r") as file:
        return json.loads(await file.read())
