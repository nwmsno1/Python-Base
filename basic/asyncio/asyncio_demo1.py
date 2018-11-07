import time
import aiohttp
import asyncio


URL = 'https://morvanzhou.github.io/'


async def job(session):
    response = await session.get(URL)
    return str(response.url)

'''如果需要并发http请求怎么办呢，通常是用requests，但requests是同步的库，如果想异步的话需要引入aiohttp。这里引入一个类，
from aiohttp import ClientSession，首先要建立一个session对象，然后用session对象去打开网页。session可以进行多项操作，
比如post, get, put, head等'''
'''首先async def 关键字定义了这是个异步函数，await 关键字加在需要等待的操作前面，response.read()等待request响应，
是个耗IO操作。然后使用ClientSession类发起http请求。'''
async def main(loop):
    async with aiohttp.ClientSession() as session:
        tasks = [loop.create_task(job(session)) for _ in range(2)]
        finished, unfinished = await asyncio.wait(tasks)
        all_results = [r.result() for r in finished]  # get return from job
        print(all_results)


t1 = time.time()
#  创建一个事件loop
loop = asyncio.get_event_loop()
# 将协程加入到事件循环loop,asyncio.get_event_loop,创建一个事件循环，
# 然后使用run_until_complete将协程注册到事件循环，并启动事件循环
loop.run_until_complete(main(loop))
loop.close()  # Ipython notebook gives error if close loop
print("Async total time:", time.time() - t1)

