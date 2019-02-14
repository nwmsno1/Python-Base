```
ser=serial.Serial("/dev/ttyUSB0",9600,timeout=0.5) #使用USB连接串行口
ser=serial.Serial("/dev/ttyAMA0",9600,timeout=0.5) #使用树莓派的GPIO口连接串行口
ser=serial.Serial(1,9600,timeout=0.5)#winsows系统使用com1口连接串行口
ser=serial.Serial("com1",9600,timeout=0.5)#winsows系统使用com1口连接串行口
ser=serial.Serial("/dev/ttyS1",9600,timeout=0.5)#Linux系统使用com1口连接串行口
print ser.name#打印设备名称
print ser.port#打印设备名
ser.open() #打开端口
s = ser.read(10)#从端口读10个字节
ser.write("hello")#向端口写数据
ser.close()#关闭端口
data = ser.read(20) #是读20个字符


data = ser.readline() #是读一行，以/n结束，要是没有/n就一直读，阻塞。

data = ser.readlines()和ser.xreadlines()#都需要设置超时时间

ser.baudrate = 9600 #设置波特率

ser.isOpen() #看看这个串口是否已经被打开
```
