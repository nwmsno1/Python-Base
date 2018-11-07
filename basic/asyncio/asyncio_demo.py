import asyncio
import time


async def job(t):  # 协程对象
    print('Start job ', t)
    # 使用async可以定义协程对象，使用await可以针对耗时的操作进行挂起，就像生成器里的yield一样，函数让出控制权。
    # 协程遇到await，事件循环将会挂起该协程，执行别的协程，直到其他的协程也挂起或者执行完毕，再进行下一个协程的执行
    await asyncio.sleep(t)  # wait for "t" seconds, it will look for another job while await
    print('Job ', t, ' takes ', t, ' s')

# 通过async关键字定义一个协程（coroutine）,当然协程不能直接运行，需要将协程加入到事件循环loop中
# asyncio.get_event_loop：创建一个事件循环，然后使用run_until_complete将协程注册到事件循环，并启动事件循环
async def main(loop):
    # 协程对象不能直接运行，在注册事件循环的时候，其实是run_until_complete方法将协程包装成为了一个任务（task）对象.
    # task对象是Future类的子类，保存了协程运行后的状态，用于未来获取协程的结果
    tasks = [loop.create_task(job(t)) for t in range(1, 3)]  # just create, not run job
    await asyncio.wait(tasks)  # run jobs and wait for all tasks done


if __name__ == '__main__':
    t1 = time.time()
    # 创建一个事件loop
    loop = asyncio.get_event_loop()
    # 将协程加入到事件循环loop
    loop.run_until_complete(main(loop))
    print("Async total time : ", time.time() - t1)
