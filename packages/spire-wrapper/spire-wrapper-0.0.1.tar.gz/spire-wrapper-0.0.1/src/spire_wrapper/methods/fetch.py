from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.join(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.resolve()))

import aiohttp
import asyncio
from dacite import from_dict
from typing import TypedDict, TypeVar, Type

from Types.Requests import Error


TimeOut = 35
T = TypeVar("T")

class fetchOptions(TypedDict):
    url: str
    headers: dict
    params: dict

async def _fetch(
    dataclassType: Type[T],
    options: fetchOptions
) -> T | Error:
    async with aiohttp.ClientSession() as session:
        async with session.get(
                options["url"],
                headers=options["headers"],
                params=options["params"]
        ) as resp:
            data = await resp.json()
            try:
                if type(data) is list:
                    return [from_dict(dataclassType, d) for d in data]
                return from_dict(dataclassType, data)
            except Exception as e:
                if len(data) == 1 and [key for key in data.keys()][0] == "detail":
                    if data["detail"] != "Not found.":
                        await asyncio.sleep(TimeOut)
                    else:
                        return from_dict(Error, data)