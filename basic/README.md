## 1. __init__和__new__的区别
__init__：通常用于初始化一个新实例，控制这个初始化的过程，比如添加一些属性， 做一些额外的操作，发生在类实例被创建完以后。
它是实例级别的方法。
__new__：通常用于控制生成一个新实例的过程。它是类级别的方法，__new__产生的实例也就是 __init__里面的的 self，然后利用这个实例来调用类的
__init__方法
__new__ 的作用:依照Python官方文档的说法，__new__方法主要是当你继承一些不可变的class时(比如int, str, tuple)， 提供给你一个自定义这些类的实例化过 
程的途径。还有就是实现自定义的metaclass。
    
example:假如我们需要一个永远都是正数的整数类型，通过集成int，我们可能会写出这样的代码
 
    class PositiveInteger(int):
        def __init__(self, value):
            super(PositiveInteger, self).__init__(self, abs(value))
       
    i = PositiveInteger(-3)
    print(i)
    result: -3
    
但运行后会发现，结果根本不是我们想的那样，我们任然得到了-3。这是因为对于int这种 不可变的对象，我们只有重载它的__new__方法才能起到自定义的作用。
    
    After modify:
    
    class PositiveInteger(int):
        def __new__(cls, value):
            return super(PositiveInteger, cls).__new__(cls, abs(value))
    i = PositiveInteger(-3)
    print(i) 
    result:3
    
通过重载__new__方法，我们实现了需要的功能。
另外一个作用，关于自定义metaclass,还可以实现单例模式

## 2. 上下文管理
当我们使用完一个资源后，我们需要手动的关闭掉它，比如操作文件，建立数据库连接等。但是，在使用资源的过程中，如果遇到异常，很可能错误被直接抛出，导致来
不及关闭资源。所以在大部分程序语言里，我们使用”try-finally”语句来确保资源会关闭
如：
    
    try:
        f = open('test.txt', 'a+')
        f.write('Foo\n')
    finally:
        f.close()
    也可以这样：
    with open('test.txt', 'a+') as f:
        f.write('Foo\n')
    
with语句后面跟着open()方法，如果它有返回值的话，可以使用as语句将其赋值给f。在with语句块退出时，”f.close()”方法会自动被调用，即使”f.write()”出
现异常，也能确保close()方法被调用。
上例中”open()”方法是Python自带的，那我们怎么定义自己的类型来使用with语句呢。其实只要你的类定义了”__enter__()”和”__exit__()”方法，就可以使用
Python的上下文管理器了。”__enter__()”方法会在with语句进入时被调用，其返回值会赋给as关键字后的变量；而”__exit__()”方法会在with语句块退出后自动
被调用。
    
    class OpenFileDemo(object):
        def __init__(self, filename):
            self.filename = filename
            
        def __enter__(self):
            self.f = open(self.filename, 'a+')
            return self.f
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.f.close()
    
    with OpenFileDemo('test.txt') as f:
        f.write('Foo\n')
    
肯定有朋友注意到上面的”__exit__()”带了三个参数，是的，他们是用来异常处理的。大部分情况下，我们希望with语句中遇到的异常最后被抛出，但也有时候，
我们想处理这些异常。”__exit__()”方法中的三个参数exc_type, exc_val, exc_tb分别代表异常类型，异常值，和异常的Traceback。当你处理完异常后，你可
以让”__exit__()”方法返回True，此时该异常就会不会再被抛出。比如我们将上例中的”__exit__()”方法改一下：
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()
        if exc_type != SyntaxError:
            return True
        return False  # Only raise exception when SyntaxError 如果遇到SyntaxError的话，异常会被正常抛出，而其他异常的话都会被忽略
Python中还有一个contextlib模块提供一些简便的上下文管理器功能
    
## 3.
