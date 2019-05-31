# 1.logging模块简介
***
logging模块定义的函数和类为应用程序和库的开发实现了一个灵活的事件日志系统。logging模块是Python的一个标准库模块，由标准库模块提供日志记
录API的关键好处是所有Python模块都可以使用这个日志记录功能。所以，你的应用日志可以将你自己的日志信息与来自第三方模块的信息整合起来。

## 1.1.logging模块的日志级别
logging模块默认定义了以下几个日志等级，它允许开发人员自定义其他日志级别，但是这是不被推荐的，尤其是在开发供别人使用的库时，因为这会导致日志级别的混乱。

日志等级（level）|描述
-|-
DEBUG|最详细的日志信息，典型应用场景是 问题诊断
INFO|信息详细程度仅次于DEBUG，通常只记录关键节点信息，用于确认一切都是按照我们预期的那样进行工作
WARNING|当某些不期望的事情发生时记录的信息（如，磁盘可用空间较低），但是此时应用程序还是正常运行的
ERROR|由于一个更严重的问题导致某些功能不能正常运行时记录的信息
CRITICAL|当发生严重错误，导致应用程序不能继续运行时记录的信息

开发应用程序或部署开发环境时，可以使用DEBUG或INFO级别的日志获取尽可能详细的日志信息来进行开发或部署调试；应用上线或部署生产环境时，应该使用WARNING或
ERROR或CRITICAL级别的日志来降低机器的I/O压力和提高获取错误日志信息的效率。日志级别的指定通常都是在应用程序的配置文件中进行指定的。

***说明：***
   
   - 上面列表中的日志等级是从上到下依次升高的，即：DEBUG < INFO < WARNING < ERROR < CRITICAL，而日志的信息量是依次减少的；
   
   - 当为某个应用程序指定一个日志级别后，应用程序会记录所有日志级别大于或等于指定日志级别的日志信息，而不是仅仅记录指定级别的日志信息，nginx、php等应
    用程序以及这里要提高的python的logging模块都是这样的。同样，logging模块也可以指定日志记录器的日志级别，只有级别大于或等于该指定日志级别的日志记
    录才会被输出，小于该等级的日志记录将会被丢弃。 

## 1.2.logging模块的使用方式介绍

logging模块提供了两种记录日志的方式：
- 第一种方式是使用logging提供的模块级别的函数
- 第二种方式是使用Logging日志系统的四大组件
其实，logging所提供的模块级别的日志记录函数也是对logging日志系统相关类的封装而已。

**logging模块定义的模块级别的常用函数**

函数|说明
:-|:-:
logging.debug(msg, *args, **kwargs)|创建一条严重级别为DEBUG的日志记录
logging.info(msg, *args, **kwargs)|创建一条严重级别为INFO的日志记录
logging.warning(msg, *args, **kwargs)|创建一条严重级别为WARNING的日志记录
logging.error(msg, *args, **kwargs)|创建一条严重级别为ERROR的日志记录
logging.critical(msg, *args, **kwargs)|创建一条严重级别为CRITICAL的日志记录
logging.log(level, *args, **kwargs)|创建一条严重级别为level的日志记录
logging.basicConfig(**kwargs)|对root logger进行一次性配置

其中`logging.basicConfig(**kwargs)`函数用于指定“要记录的日志级别”、“日志格式”、“日志输出位置”、“日志文件的打开模式”等信息，其他几个都是用于记录
各个级别日志的函数。

**logging模块的四大组件**

组件|说明
-:|:-:
loggers|提供应用程序代码直接使用的接口
handler|用于将日志记录发送到指定的目的位置
filters|提供更细粒度的日志过滤功能，用于决定哪些日志记录将会被输出（其它的日志记录将会被忽略）
formatters|用于控制日志信息的最终输出格式

***说明：*** *logging模块提供的模块级别的那些函数实际上也是通过这几个组件的相关实现类来记录日志的，只是在创建这些类的实例时设置了一些默认值*

# 2.使用logging提供的模块级别的函数记录日志
---
回顾下前面提到的几个重要信息：
- 可以通过logging模块定义的模块级别的方法去完成简单的日志记录
- 只有级别大于或等于日志记录器指定级别的日志记录才会被输出，小于该级别的日志记录将会被丢弃。

## 2.1.最简单的日志输出

先来试着分别输出一条不同日志级别的日志记录：
```
import logging

logging.debug("This is a debug log.")
logging.info("This is a info log.")
logging.warning("This is a warning log.")
logging.error("This is a error log.")
logging.critical("This is a critical log.")
```

也可以这样写：
```
logging.log(logging.DEBUG, "This is a debug log.")
logging.log(logging.INFO, "This is a info log.")
logging.log(logging.WARNING, "This is a warning log.")
logging.log(logging.ERROR, "This is a error log.")
logging.log(logging.CRITICAL, "This is a critical log.")
```
输出结果：
```
WARNING:root:This is a warning log.
ERROR:root:This is a error log.
CRITICAL:root:This is a critical log.
```

## 3.2.那么问题来了
### 问题1：为什么前面两条日志没有被打印出来？
这是因为logging模块提供的日志记录函数所使用的日志器设置的日志级别是WARNING，因此只有WARNING级别的日志记录以及大于它的ERROR和CRITICAL级别的日志记录被输出了，而小于它的DEBUG和INFO级别的日志记录被丢弃了。
### 问题2：打印出来的日志信息中各字段表示什么意思？为什么会这样输出？
上面输出结果中每行日志记录的各个字段含义分别是：
`日志级别:日志器名称:日志内容`
之所以会这样输出，是因为logging模块提供的日志记录函数所使用的日志器设置的日志格式默认是BASIC_FORMAT，其值为：
`"%(levelname)s:%(name)s:%(message)s"`
### 问题3：如果将日志记录输出到文件中，而不是打印到控制台？
因为在logging模块提供的日志记录函数所使用的日志器设置的处理器所指定的日志输出位置默认为:
`sys.stderr`
### 问题4：我是怎么知道这些的？
查看这些日志记录函数的实现代码，可以发现：当我们没有提供任何配置信息的时候，这些函数都会去调用logging.basicConfig(**kwargs)方法，且不会向该方法传递任何参数。继续查看basicConfig()方法的代码就可以找到上面这些问题的答案了。
### 问题5：怎么修改这些默认设置呢？
其实很简单，在我们调用上面这些日志记录函数之前，手动调用一下basicConfig()方法，把我们想设置的内容以参数的形式传递进去就可以了。

## 2.3.logging.basicConfig()函数说明
该方法用于为logging日志系统做一些基本配置，方法定义如下：
`logging.basicConfig(**kwargs)`

该函数可接收的关键字参数如下：


参数名称|描述
:-|:-
filename|指定日志输出目标文件的文件名，指定该设置项后日志信心就不会被输出到控制台了
filemode|指定日志文件的打开模式，默认为'a'。需要注意的是，该选项要在filename指定时才有效
format|指定日志格式字符串，即指定日志输出时所包含的字段信息以及它们的顺序。logging模块定义的格式字段下面会列出。
datefmt|指定日期/时间格式。需要注意的是，该选项要在format中包含时间字段%(asctime)s时才有效
level|指定日志器的日志级别
stream|指定日志输出目标stream，如sys.stdout、sys.stderr以及网络stream。需要说明的是，stream和filename不能同时提供，否则会引发 ValueError异常
style|Python 3.2中新添加的配置项。指定format格式字符串的风格，可取值为'%'、'{'和'$'，默认为'%'
handlers|Python 3.3中新添加的配置项。该选项如果被指定，它应该是一个创建了多个Handler的可迭代对象，这些handler将会被添加到root logger。需要说明的是：filename、stream和handlers这三个配置项只能有一个存在，不能同时出现2个或3个，否则会引发ValueError异常。

## 2.4. logging模块定义的格式字符串字段

我们来列举一下logging模块中定义好的可以用于format格式字符串中字段有哪些：

字段/属性名称|使用格式|描述
:-|:-|:-
asctime|%(asctime)s|日志事件发生的时间--人类可读时间，如：2003-07-08 16:49:45,896
created|%(created)f|日志事件发生的时间--时间戳，就是当时调用time.time()函数返回的值
relativeCreated|%(relativeCreated)d|日志事件发生的时间相对于logging模块加载时间的相对毫秒数（目前还不知道干嘛用的）
msecs|%(msecs)d|日志事件发生事件的毫秒部分
levelname|%(levelname)s|该日志记录的文字形式的日志级别（'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'）
levelno|%(levelno)s|该日志记录的数字形式的日志级别（10, 20, 30, 40, 50）
name|%(name)s|所使用的日志器名称，默认是'root'，因为默认使用的是 rootLogger
message|%(message)s|日志记录的文本内容，通过 msg % args计算得到的
pathname|%(pathname)s|调用日志记录函数的源码文件的全路径
filename|%(filename)s|pathname的文件名部分，包含文件后缀
module|%(module)s|filename的名称部分，不包含后缀
lineno|%(lineno)d|调用日志记录函数的源代码所在的行号
funcName|%(funcName)s|调用日志记录函数的函数名
process|%(process)d|进程ID
processName|%(processName)s|进程名称，Python 3.1新增
thread|%(thread)d|线程ID
threadName|%(thread)s|线程名称

## 2.5.经过配置的日志输出
先简单配置下日志器的日志级别
```
logging.basicConfig(level=logging.DEBUG)

logging.debug("This is a debug log.")
logging.info("This is a info log.")
logging.warning("This is a warning log.")
logging.error("This is a error log.")
logging.critical("This is a critical log.")
```
输出结果：
```
DEBUG:root:This is a debug log.
INFO:root:This is a info log.
WARNING:root:This is a warning log.
ERROR:root:This is a error log.
CRITICAL:root:This is a critical log.
```
所有等级的日志信息都被输出了，说明配置生效了。
在配置日志器日志级别的基础上，在配置下日志输出目标文件和日志格式
```
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)

logging.debug("This is a debug log.")
logging.info("This is a info log.")
logging.warning("This is a warning log.")
logging.error("This is a error log.")
logging.critical("This is a critical log.")
```
此时会发现控制台中已经没有输出日志内容了，但是在python代码文件的相同目录下会生成一个名为'my.log'的日志文件，该文件中的内容为:
```
2017-05-08 14:29:53,783 - DEBUG - This is a debug log.
2017-05-08 14:29:53,784 - INFO - This is a info log.
2017-05-08 14:29:53,784 - WARNING - This is a warning log.
2017-05-08 14:29:53,784 - ERROR - This is a error log.
2017-05-08 14:29:53,784 - CRITICAL - This is a critical log.
```
在上面的基础上，我们再来设置下日期/时间格式
```
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

logging.debug("This is a debug log.")
logging.info("This is a info log.")
logging.warning("This is a warning log.")
logging.error("This is a error log.")
logging.critical("This is a critical log.")
```
此时会在my.log日志文件中看到如下输出内容：
```
05/08/2017 14:29:04 PM - DEBUG - This is a debug log.
05/08/2017 14:29:04 PM - INFO - This is a info log.
05/08/2017 14:29:04 PM - WARNING - This is a warning log.
05/08/2017 14:29:04 PM - ERROR - This is a error log.
05/08/2017 14:29:04 PM - CRITICAL - This is a critical log.
```
掌握了上面的内容之后，已经能够满足我们平时开发中需要的日志记录功能。

## 2.6. 其他说明
几个要说明的内容:
- logging.basicConfig()函数是一个一次性的简单配置工具使，也就是说只有在第一次调用该函数时会起作用，后续再次调用该函数时完全不会产生任何操作的，多次调用的设置并不是累加操作。
- 日志器（Logger）是有层级关系的，上面调用的logging模块级别的函数所使用的日志器是RootLogger类的实例，其名称为'root'，它是处于日志器层级关系最顶层的日志器，且该实例是以单例模式存在的。
- 如果要记录的日志中包含变量数据，可使用一个格式字符串作为这个事件的描述消息（logging.debug、logging.info等函数的第一个参数），然后将变量数据作为第二个参数*args的值进行传递，如:logging.warning('%s is %d years old.', 'Tom', 10)，输出内容为WARNING:root:Tom is 10 years old.
- logging.debug(), logging.info()等方法的定义中，除了msg和args参数外，还有一个**kwargs参数。它们支持3个关键字参数: exc_info, stack_info, extra，下面对这几个关键字参数作个说明。

关于exc_info, stack_info, extra关键词参数的说明:
- exc_info： 其值为布尔值，如果该参数的值设置为True，则会将异常异常信息添加到日志消息中。如果没有异常信息则添加None到日志信息中。
- stack_info： 其值也为布尔值，默认值为False。如果该参数的值设置为True，栈信息将会被添加到日志信息中。
- extra： 这是一个字典（dict）参数，它可以用来自定义消息格式中所包含的字段，但是它的key不能与logging模块定义的字段冲突。

一个例子：
在日志消息中添加exc_info和stack_info信息，并添加两个自定义的字端 ip和user
```
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(user)s[%(ip)s] - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(format=LOG_FORMAT, datefmt=DATE_FORMAT)
logging.warning("Some one delete the log file.", exc_info=True, stack_info=True, extra={'user': 'Tom', 'ip':'47.98.53.222'})
```
输出结果：
```
05/08/2017 16:35:00 PM - WARNING - Tom[47.98.53.222] - Some one delete the log file.
NoneType
Stack (most recent call last):
  File "C:/Users/wader/PycharmProjects/LearnPython/day06/log.py", line 45, in <module>
    logging.warning("Some one delete the log file.", exc_info=True, stack_info=True, extra={'user': 'Tom', 'ip':'47.98.53.222'})
```

