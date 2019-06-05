"""线程的运行是独立的，如果线程间需要通信，或者说某个线程需要根据一个线程的状态来执行下一步的操作，就需要用到Event对象。可以把Event对象看作是
一个标志位，默认值为假，如果一个线程等待Event对象，而此时Event对象中的标志位为假，那么这个线程就会一直等待，直至标志位为真，为真以后，所有等待
Event对象的线程将被唤醒"""


import threading, time

event = threading.Event()  # 创建一个event对象


def foo():
    print('waiting...')
    event.wait()
    # event.wait(1) if event 对象内的标志位为Flase,则阻塞
    # wait()里面的参数的意思是：只等待1秒，如果1秒后还没有把标志位改过来，就不等了，继续执行下面的代码
    print('connect to redis server')


if __name__ == '__main__':
    
    print('attempt to start redis sever)')
    time.sleep(3)
    event.set()  # 设置event的状态值为True，所有阻塞池的线程激活进入就绪状态， 等待操作系统调度；设置对象的时候，默认是False的
    
    for i in range(5):
        t = threading.Thread(target=foo, args=())
        t.start()
    
    # 3秒之后，主线程结束，但子线程并不是守护线程，子线程还没结束，所以，程序并没有结束，应该是在3秒之后，把标志位设为true，即event.set（）
