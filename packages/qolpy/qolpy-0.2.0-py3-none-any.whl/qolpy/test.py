from . import Logger
import time
import asyncio
from typing_extensions import List

instance = Logger()


@instance.lax
async def bro(name: List[str]):
    instance.log("stats", "test", "chained?")
    time.sleep(1)
    print("done")


asyncio.run(bro(name=["one", "two"]))

# bro()
