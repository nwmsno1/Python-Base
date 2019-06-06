# 这个模块封装了yield，使得程序切换非常方便，但是没法实现传值的功能


from greenlet import greenlet


def foo():
    print('ok1')
    gr2.switch()
    print('ok3')
    gr2.switch()


def bar():
    print('ok2')
    gr1.switch()
    print('ok4')


if __name__ == '__main__':
    gr1 = greenlet(foo)
    gr2 = greenlet(bar)

    gr1.switch()  # 启动


"""
result:
C:\ProgramData\Anaconda3\python.exe C:/testcases/test/asyncio_greenlet.py
ok1
ok2
ok3
ok4

Process finished with exit code 0
"""
