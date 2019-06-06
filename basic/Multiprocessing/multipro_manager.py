# 进程间的数据共享需要引用一个manager对象实现，使用的所有的数据类型都要通过manager点的方式去创建

from multiprocessing import Process, Manager


def foo(l, i):
    l.append(i*i)
    

if __name__ == '__main__':
    manager = Manager()
    
    mlist = manager.list([1, 2, 3, 4])  # 创建一个共享的列表
    
    l = []
    
    for i in range(5):  # 开辟5个子进程
        p = Process(target=foo, args=(mlist, i))
        p.start()
        l.append(p)
    
    for i in l:
        i.join()  # join 方法是等待进程结束后再执行下一个
    print(mlist)
