import time


class Door():
    address = '南京'
    def __init__(self, size, color, type):  # 构造函数
        self.size = size
        self.color = color
        self.type = type
    
    @property
    def open(self):
        print("这个%s门打开了" %self.type)
    
    @property
    def close(self, time):
        print("这个%s门关闭了,时间为；%s" %(self.type,time))
    

if __name__ == '__main__':
    door = Door(16, 'red', '木门')
    # 调用数据属性
    print('door.size')
    print('door.address')
    # 调用函数属性
    # door.open()    # 函数后面的括号每次都必须要带上
    # 实例调用类的静态属性
    print(Door.__dict__)
    door.open
    time1 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    # door.close(time1)    #传参无效，应该要自定义对应的装饰器才行
