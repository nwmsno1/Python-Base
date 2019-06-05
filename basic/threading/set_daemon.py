import  threading
import time

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('ok')
        time.sleep(2)
        print('end')
# 默认情况下，主线程运行完会检查子线程是否完成，如果未完成，那么主线程会等待子线程完成后再退出。
# 但是如果主线程完成后不用管子线程是否运行完都退出，就要设置setDaemon（True）

t1=MyThread()  # 创建线程对象
t1.setDaemon(True)  # 这个方法的作用是把线程声明为守护线程，必须在start()方法调用之前设置。
t1.start()  # 激活线程对象
print('end again')
#运行结果是马上打印ok和 end again 
#然后程序终止，不会打印end
