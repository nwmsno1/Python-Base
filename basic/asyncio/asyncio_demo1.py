import time
import aiohttp
import asyncio


URL = 'https://morvanzhou.github.io/'


async def job(session):
    response = await session.get(URL)
    return str(response.url)


async def main(loop):
    async with aiohttp.ClientSession() as session:
        tasks = [loop.create_task(job(session)) for _ in range(2)]
        finished, unfinished = await asyncio.wait(tasks)
        all_results = [r.result() for r in finished]  # get return from job
        print(all_results)


t1 = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
# loop.close()  # Ipython notebook gives error if close loop
print("Async total time:", time.time() - t1)

