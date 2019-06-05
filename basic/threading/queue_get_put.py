"""官方文档说队列在多线程中保证数据安全是非常有用的,队列可以理解为是一种数据结构，
可以存储数据，读写数据。就类似列表里面加了一把锁"""

import queue

# 队列里读写数据只有put和get两个方法，列表的那些方法都没有
q = queue.Queue()  # 创建一个队列对象 FIFO先进先出
# q=queue.Queue(20)
# 这里面可以有一个参数，设置最大存的数据量，可以理解为最大有几个格子
# 如果设置参数为20，第21次put的时候，程序就会阻塞住，直到有空位置，也就是有数据被get走

q.put(11)  # 放值
q.put('hello')
q.put(3.14)

print(q.get())  # 取值11
print(q.get())  # 取值hello
print(q.get())  # 取值3.14
print(q.get())  # 阻塞，等待put一个数据
# get方法中有个默认参数block=True,把这个参数改成False,取不到值的时候就会报错queue.Empty
