"""协程在手，天下我有，说走就走。协程就有点牛逼了

协程可以开很多很多，没有上限，切换之间的消耗可以忽略不计"""

"""yield是个挺神奇的东西，这是Python的一个特点。

一般的函数，是遇到return就停止，然后返回return 后面的值，默认是None，yield和return很像，但是遇到yield不会立刻停止，
而是暂停住，直到遇到next()，(for循环的原理也是next()) 才会继续执行。yield 前面还可以跟一个变量，通过send()函数给yield传
值，把值保存在yield前边的变量中"""


import time


def consumer():  # 有yield，是一个生成器
    r = ""
    while True:
        n = yield r  # 返回r,程序暂停，等待next()信号

        print('consumer <--%s..' % n)
        time.sleep(1)
        r = '200 ok'


def producer(c):
    next(c)  # 激活生成器c
    n = 0
    while n < 5:
        n = n + 1
        print('producer-->%s..' % n)
        cr = c.send(n)  # 向生成器发送数据
        print('consumer return :', cr)
    c.close()  # 生产过程结束，关闭生成器


if __name__ == '__main__':
    c = consumer()
    producer(c)
    

"""看上面的例子，整个过程没有锁的出现，还能保证数据安全，更要命的是还可以控制顺序，优雅的实现了并发，甩多线程几条街

线程叫微进程，而协程又叫微线程。协程拥有自己的寄存器上下文和栈，因此能保留上一次调用的状态。"""
