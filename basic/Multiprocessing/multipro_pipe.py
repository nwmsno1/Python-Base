# socket其实就是管道，客户端 的sock和服务端的conn是管道 的两端，在进程中也是这个玩法，也要有管道的两头

from multiprocessing import Pipe, Process


def foo(sk):
    sk.send('hello')  # 主进程发消息
    print(sk.recv())  # 主进程收消息


if __name__ == '__main__':
    sock, conn = Pipe()  # 创建了管道的两头
    p = Process(target=foo, args=(sock,))
    p.start()

    print(conn.recv())  # 子进程接收消息
    conn.send('hi, son')  # 子进程发消息
