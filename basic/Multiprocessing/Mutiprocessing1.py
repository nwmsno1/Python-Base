# python 中有一把全局锁（GIL）使得多线程无法使用多核，但是如果是多进程，这把锁就限制不了了。如何开多个进程呢，需要导入一个

import multiprocessing as mp


def job(q):
    res = 0
    for i in range(100000):
        res += i + i**2 + i**3
    q.put(res)


def main():
    q = mp.Queue()
    p1 = mp.Process(target=job, args=(q,))
    p2 = mp.Process(target=job, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    res1 = q.get()
    res2 = q.get()
    print(res1+res2)


if __name__ == '__main__':
    main()
