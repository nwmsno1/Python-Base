# 进程池的作用是维护一个最大的进程量，如果超出设置的最大值，程序就会阻塞，直到有可用的进程为止

from multiprocessing import Pool

import time


def foo(n):
    print(n)
    time.sleep(2)


if __name__ == '__main__':
    pool_obj = Pool(5)  # 创建进程池

    # 通过进程池创建进程
    for i in range(5):
        p = pool_obj.apply_async(func=foo, args=(i,))  # p是创建的池对象

    # pool 的使用是先close()，在join（）,记住就行了
    pool_obj.close()
    pool_obj.join()

    print('ending')
    

"""
result:
C:\Users\TS\Anaconda3\python.exe C:/Users/TS/PycharmProjects/opencv_py/数据预处理.py
0
1
2
3
4
ending

Process finished with exit code 0
"""

"""
进程池中有以下几个方法：

1.apply：从进程池里取一个进程并执行
2.apply_async：apply的异步版本
3.terminate:立刻关闭线程池
4.join：主进程等待所有子进程执行完毕，必须在close或terminate之后
5.close：等待所有进程结束后，才关闭线程池
"""
