# 进程间通信有两种方式，队列和管道,Queue用于多个进程间实现通信，Pipe是两个进程的通信
# 进程间的队列
# 每个进程在内存中都是独立的一块空间，不像线程那样可以共享数据，所以只能由父进程通过传参的方式把队列传给子进程


import multiprocessing
from multiprocessing import Queue


def foo(q):
    q.put([12, 'hello', True])


if __name__ == '__main__':
    q = Queue()  # 创建进程队列

    # 创建一个子进程
    p = multiprocessing.Process(target=foo, args=(q,))
    # 通过传参的方式把这个队列对象传给父进程
    p.start()

    print(q.get())
