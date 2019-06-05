# 死锁就是两个及以上进程或线程在执行过程中，因相互制约造成的一种互相等待的现象，若无外力作用，他们将永远卡在那里

import threading, time


class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.foo()
        self.bar()

    def foo(self):
        LockA.acquire()
        print('i am %s GET LOCKA------%s' % (self.name, time.ctime()))  # 每个线程有个默认的名字，self.name就获取这个名字

        LockB.acquire()
        print('i am %s GET LOCKB-----%s' % (self.name, time.ctime()))

        LockB.release()
        time.sleep(1)
        LockA.release()

    def bar(self):
        LockB.acquire()
        print('i am %s GET LOCKB------%s' % (self.name, time.ctime()))  # 每个线程有个默认的名字，self.name就获取这个名字

        LockA.acquire()
        print('i am %s GET LOCKA-----%s' % (self.name, time.ctime()))

        LockA.release()
        LockB.release()


if __name__ == '__main__':
    LockA = threading.Lock()
    LockB = threading.Lock()

    for i in range(10):
        t = MyThread()
        t.start()
 
"""result:
C:\ProgramData\Anaconda3\python.exe C:/testcases/test/thread_deadlock.py
i am Thread-1 GET LOCKA------Wed Jun  5 18:20:24 2019
i am Thread-1 GET LOCKB-----Wed Jun  5 18:20:24 2019
i am Thread-1 GET LOCKB------Wed Jun  5 18:20:25 2019
i am Thread-2 GET LOCKA------Wed Jun  5 18:20:25 2019
卡住了"""

"""上面这个例子中，线程2在等待线程1释放B锁，线程1在等待线程2释放A锁，互相制约.我们在用互斥锁的时候，一旦用的锁多了，很容易就出现这种问题.
在Python中，为了解决这个问题，Python提供了一个叫可重用锁（RLock）的概念，这个锁内部维护着一个lock和一个counter变量，counter记录了acquire的次数，
每次acquire，counter就加1，每次release,counter就减1，只有counter的值为0的时候，其他线程才能获得资源，下面用RLock替换Lock，在运行就不会卡住了,这把
锁又叫递归锁"""

import threading, time


class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.foo()
        self.bar()

    def foo(self):
        RLock.acquire()
        print('i am %s GET LOCKA------%s' % (self.name, time.ctime()))  # 每个线程有个默认的名字，self.name就获取这个名字

        RLock.acquire()
        print('i am %s GET LOCKB-----%s' % (self.name, time.ctime()))

        RLock.release()
        time.sleep(1)
        RLock.release()

    def bar(self):
        RLock.acquire()
        print('i am %s GET LOCKB------%s' % (self.name, time.ctime()))  # 每个线程有个默认的名字，self.name就获取这个名字

        RLock.acquire()
        print('i am %s GET LOCKA-----%s' % (self.name, time.ctime()))

        RLock.release()
        RLock.release()


if __name__ == '__main__':
    LockA = threading.Lock()
    LockB = threading.Lock()
    RLock = threading.RLock()
    for i in range(10):
        t = MyThread()
        t.start()
