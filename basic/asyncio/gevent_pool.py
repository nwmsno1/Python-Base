# gevent模块中还有协程池

from gevent.pool import Pool
import gevent
import requests


def get_page(url):

    response=requests.get(url)
    response_str=response.text

    print('get data %s' % len(response_str))


if __name__ == '__main__':

    pool = Pool(2)

    g1 = pool.spawn(get_page, 'https://itk.org/')
    g2 = pool.spawn(get_page, "https://www.github.com/")
    g3 = pool.spawn(get_page, "https://zhihu.com/")

    gevent.joinall([g1, g3, g2, ])
    print(g1.value, g2.value, g3.value)


"""
协程的优缺点：
优点：

　　上下文切换消耗小

　　方便切换控制流，简化编程模型

　　高并发，高扩展性，低成本

缺点：

　　无法利用多核

　　进行阻塞操作时会阻塞掉整个程序

 　　单纯的协程是没有意义的，只是人为的控制执行一下这个，执行一下那个，如果想监测是否有IO操作，需要结合IO多路复用（select/poll/epoll）
"""
