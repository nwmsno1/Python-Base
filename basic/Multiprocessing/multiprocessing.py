# python 中有一把全局锁（GIL）使得多线程无法使用多核，但是如果是多进程，这把锁就限制不了了。如何开多个进程呢，需要导入一个


import multiprocessing
import time

def foo():
    print('ok')
    time.sleep(2)
    
    
if __name__ == "__main__":
    p = multiprocessing.Process(target=foo, args=())
    p.start()
    print('ending')
    
"""虽然可以开多进程，但是一定注意进程不能开太多，因为进程间切换非常消耗系统资源，如果开上千个子进程，系统会崩溃的,
而且进程间的通信也是个问题。所以，进程能不用就不用，能少用就少用"""
