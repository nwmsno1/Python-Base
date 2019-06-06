"""
在greenlet模块的基础上，开发出了更牛的模块gevent

gevent为Python提供了更完善的协程支持，其基本原理是：

当一个greenlet遇到IO操作时，就会自动切换到其他的greenlet,等IO操作完成，再切换回来，这样就保证了总有greenlet在运行，而不是等待
"""


import requests
import gevent
import time


def foo(url):

    response = requests.get(url)
    response_str = response.text
    
    print('get data %s' % len(response_str))


if __name__ == '__main__':
    s = time.time()
    gevent.joinall([gevent.spawn(foo, "https://itk.org/"),
                    gevent.spawn(foo, "https://www.github.com/"),
                    gevent.spawn(foo, "https://zhihu.com/"), ])
    print(time.time() - s)
   
