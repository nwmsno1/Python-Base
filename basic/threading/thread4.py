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
