# 需求是有一个全局变量的值是100，我们开100个线程，每个线程执行的操作是对这个全局变量减一，最后值减为0

import threading
import time


def sub():
    global num
    tmp = num
    num = tmp - 1
    time.sleep(2)


if __name__ == "__main__":
    num = 100
    l = []
    for i in range(100):
        t = threading.Thread(target=sub)
        t.start()
        l.append(t)
    for j in l:
        j.join()
    print(num)


"""好像一切正常，现在我们改动一下，在sub函数的temp=num,
和num=temp-1 中间，加一个time.sleep(0.1),会发现出问题了，结果变成两秒后打印99了，改成time.sleep(0.0001)呢，
结果不确定了，但都是90,这就要说到Python里的那把GIL锁了"""

"""首次定义一个全局变量num=100,然后开辟了100个子线程，但是Python的那把GIL锁限制了同一时刻只能有一个线程使用cpu，所以这100个线程是处于抢这把锁的
状态，谁抢到了，谁就可以运行自己的代码。在最开始的情况下，每个线程抢到cpu，马上执行了对全局变量减一的操作，所以不会出现问题。但是我们改动后，在全
局变量减一之前，让他睡了0.1秒，程序睡着了，cpu可不能一直等着这个线程，当这个线程处于I/O阻塞的时候，其他线程就又可以抢cpu了，所以其他线程抢到了，
开始执行代码，要知道0.1秒对于cpu的运行来说已经很长时间了，这段时间足够让第一个线程还没睡醒的时候，其他线程都抢到过cpu一次了。他们拿到的num都是100，
等他们醒来后，执行的操作都是100-1,所以最后结果是99.同样的道理，如果睡的时间短一点，变成0.001，可能情况就是当第91个线程第一次抢到cpu的时候，第一个
线程已经睡醒了，并修改了全局变量。所以这第91个线程拿到的全局变量就是99，然后第二个第三个线程陆续醒过来，分别修改了全局变量，所以最后结果就是一个不
可知的数了。"""
"""这就是线程安全问题，只要涉及到线程，都会有这个问题。解决办法就是加锁

我们在全局加一把锁，用锁把涉及到数据运算的操作锁起来，就把这段代码变成串行的了，上代码："""

# 获取这把锁之后，必须释放掉才能再次被获取。这把锁就叫用户锁

import threading
import time


def sub():
    global num
    lock.acquire()  # 获取锁
    temp = num
    time.sleep(0.01)
    num = temp - 1
    lock.release()  # 释放锁
    time.sleep(2)

num = 100
l = []
for i in range(100):
    t = threading.Thread(target=sub)
    t.start()
    l.append(t)
for j in l:
    j.join()
print(num)
    
