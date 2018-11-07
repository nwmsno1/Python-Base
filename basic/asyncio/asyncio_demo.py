import asyncio
import time


async def job(t):  # 协程对象
    print('Start job ', t)
    await asyncio.sleep(t)  # wait for "t" seconds, it will look for another job while await
    print('Job ', t, ' takes ', t, ' s')


async def main(loop):
    # 协程对象不能直接运行，在注册事件循环的时候，其实是run_until_complete方法将协程包装成为了一个任务（task）对象.
    # task对象是Future类的子类，保存了协程运行后的状态，用于未来获取协程的结果
    tasks = [loop.create_task(job(t)) for t in range(1, 3)]  # just create, not run job
    await asyncio.wait(tasks)  # run jobs and wait for all tasks done


if __name__ == '__main__':
    t1 = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    print("Async total time : ", time.time() - t1)
