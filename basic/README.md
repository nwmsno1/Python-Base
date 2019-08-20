## 1. \_\_init\_\_和\_\_new\_\_的区别
***
\_\_init\_\_：通常用于初始化一个新实例，控制这个初始化的过程，比如添加一些属性， 做一些额外的操作，发生在类实例被创建完以后。
它是实例级别的方法。

\_\_new\_\_：通常用于控制生成一个新实例的过程。它是类级别的方法，\_\_new\_\_产生的实例也就是\_\_init\_\_里面的的 self，然后利用这个实例来调用类的\__init__方法

\_\_new\_\_ 的作用:依照Python官方文档的说法，\_\_new\_\_方法主要是当你继承一些不可变的class时(比如int, str, tuple)， 提供给你一个自定义这些类的实例化过程的途径。还有就是实现自定义的metaclass。
    
example:假如我们需要一个永远都是正数的整数类型，通过集成int，我们可能会写出这样的代码
 
    class PositiveInteger(int):
        def __init__(self, value):
            super(PositiveInteger, self).__init__(self, abs(value))
       
    i = PositiveInteger(-3)
    print(i)
    result: -3
    
但运行后会发现，结果根本不是我们想的那样，我们任然得到了-3。这是因为对于int这种 不可变的对象，我们只有重载它的\_\_new\_\_方法才能起到自定义的作用。
    
    After modify:
    
    class PositiveInteger(int):
        def __new__(cls, value):
            return super(PositiveInteger, cls).__new__(cls, abs(value))
    i = PositiveInteger(-3)
    print(i) 
    result:3
    
通过重载\_\_new\_\_方法，我们实现了需要的功能。
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
    
## 3. python3中函数和方法的区别

```
def mytest():
    pass


class People():

    def jump(self):
        print('jumpping ....')

    @staticmethod
    def speak(self):
        print('speaking....')

    @classmethod
    def run(cls):
        print('running....')


if __name__ == '__main__':
    print(type(mytest))
    print('=====================================')

    p = People()

    print(type(p.jump))
    print(type(People.jump))
    print('=====================================')

    print(type(p.speak))
    print(type(People.speak))
    print('=====================================')

    print(type(p.run))
    print(type(People.run))
    print('=====================================')
    
    
    
    <class 'function'>
    =====================================
    <class 'method'>
    <class 'function'>
    =====================================
    <class 'function'>
    <class 'function'>
    =====================================
    <class 'method'>
    <class 'method'>
    =====================================
```

当你向jump中传入的首参为People的实例时，jump就是方法.而当你传入的首参不是People的实例对象时，jump就是函数

```
p = People()
People.jump('hello')
jumpping ....
People.jump(p)
jumpping ....
```
总结一下，在Python3中：
1. 普通函数（未定义在类中），都是函数
2. 静态方法（@staticmethod），都是函数
3. 类方法（@classmethod），都是方法
4. 方法和函数区分没有那么明确，而是更加灵活了，一个函数有可能时方法也有可能是函数

## 4. 闭包
***
python中的闭包从表现形式上定义（解释）为：如果在一个内部函数中，对在外部作用域（但不是在全局作用域，非局部变量）的变量进行引用，那么内部函数就被认为是闭包（closure).
```
>>>def addx(x):
>>>    def adder(y):
>>>        return x + y
>>>    return adder
>>> c =  addx(8)
>>> type(c)
<type 'function'>
>>> c.__name__
'adder'
>>> c(10)
18
```

如果在一个内部函数中：adder(y)就是这个内部函数. 对于外部作用域（非全局作用域，非局部变量）的变量进行引用，x就是被引用的变量，x在外部作用域addx中，但不在全局作用域中，则这个内部函数adder就是一个闭包

### 1.在闭包中是不能修改外部作用域的局部变量的
```
>>> def foo():
...     m = 0
...     def foo1():
...         m = 1
...         print m
...
...     print m
...     foo1()
...     print m
...
>>> foo()
0
1
0
```
从执行结果看，虽然在闭包里也定义了一个变量m，但是其不会改变外部函数中的的局部变量m.

### 2.以下这段代码是在python中使用闭包时一段经典的错误代码
```
def foo():
    a = 1
    def bar():
        a = a + 1
        return a
    return bar
```
这段程序的本意是要通过在每次调用闭包函数时都对变量a进行递增的操作。但在实际使用时

    >>> c = foo()
    >>> print c()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 4, in bar
    UnboundLocalError: local variable 'a' referenced before assignment

这是因为在执行代码 c = foo()时，python会导入全部的闭包函数体bar()来分析其的局部变量，python规则指定所有在赋值语句左面的变量都是局部变量，则在闭包bar()中，变量a在赋值符号"="的左面，被python认为是bar()中的局部变量。再接下来执行print c()时，程序运行至a = a + 1时，因为先前已经把a归为bar()中的局部变量，所以python会在bar()中去找在赋值语句右面的a的值，结果找不到，就会报错。
解决的方法很简单，你可以简单认为，可变对象（即我们可以通过调用自身一些方法去做增删改操作且变量地址不变）不存在此问题.而不可变对象则会有
```
def foo():
    a = [1]
    def bar():
        a[0] = a[0] + 1
        return a[0]
    return bar
```
```
class A():
    pass

def foo():
    a = A()
    a.value = 1
    def bar():
        a.value += 1
        return a.value
    return bar

c = foo()
print(c())
```
只要将a设定为一个容器就可以了,或者所以在python3以后，在a = a + 1 之前，使用语句nonlocal a就可以了，该语句显式的指定a不是闭包的局部变量

```
def foo():
    a = 1
    def bar():
        nonlocal a
        a = a + 1
        return a
    return bar

c = foo()
c
Out[24]: <function __main__.foo.<locals>.bar>
c()
Out[25]: 2
```
### 3.用途
闭包主要是在函数式开发过程中使用。以下介绍两种闭包主要的用途
#### 用途1，当闭包执行完后，仍然能够保持住当前的运行环境
比如说，如果你希望函数的每次执行结果，都是基于这个函数上次的运行结果。我以一个类似棋盘游戏的例子来说明。假设棋盘大小为50\*50，左上角为坐标系原点(0,0)，我需要一个函数，接收2个参数，分别为方向(direction)，步长(step)，该函数控制棋子的运动。棋子运动的新的坐标除了依赖于方向和步长以外，当然还要根据原来所处的坐标点，用闭包就可以保持住这个棋子原来所处的坐标
```
origin = [0, 0]  # 坐标系统原点
legal_x = [0, 50]  # x轴方向的合法坐标
legal_y = [0, 50]  # y轴方向的合法坐标
def create(pos=origin):
    def player(direction,step):
        # 这里应该首先判断参数direction,step的合法性，比如direction不能斜着走，step不能为负等
        # 然后还要对新生成的x，y坐标的合法性进行判断处理，这里主要是想介绍闭包，就不详细写了
        new_x = pos[0] + direction[0]*step
        new_y = pos[1] + direction[1]*step
        pos[0] = new_x
        pos[1] = new_y
        # 注意！此处不能写成 pos = [new_x, new_y]，原因是赋值操作，在上文有说过,
        return pos
    return player
 
player = create()  # 创建棋子player，起点为原点
print player([1,0],10)  # 向x轴正方向移动10步
print player([0,1],20)  # 向y轴正方向移动20步
print player([-1,0],10)  # 向x轴负方向移动10步

[10, 0]
[10, 20]
[0, 20]
```
#### 用途2，闭包可以根据外部作用域的局部变量来得到不同的结果，这有点像一种类似配置功能的作用，我们可以修改外部的变量，闭包根据这个变量展现出不同的功能。比如有时我们需要对某些文件的特殊行进行分析，先要提取出这些特殊行
```
def make_filter(keep):
    def the_filter(file_name):
        file = open(file_name)
        lines = file.readlines()
        file.close()
        filter_doc = [i for i in lines if keep in i]
        return filter_doc
    return the_filter
  ```
如果我们需要取得文件"result.txt"中含有"pass"关键字的行，则可以这样使用例子程序
```
filter = make_filter("pass")
filter_result = filter("result.txt")
```

## 5. 深拷贝与浅拷贝


## 6. 类继承问题
有如下一段代码：
```
class A(object):
    def show(self):
        print("base show")
    
class B(A):
    def show(self):
        print("derived show")

obj = B()
obj.show()
```

如何调用类A的show方法了， 方法如下：
```
obj.__class__ = A
obj.show()
```
`__class_`方法指向了类对象，只用给他赋值类型A,然后调用方法show,但是用完了记得修改回来

## 7. 方法对象
问题：为了让下面这段代码运行，需要增加哪些代码?
```
class A(object):
    def __init__(self, a, b):
        self.__a = a
        self.__b = b
    
    def myprint(self):
        print('a = ', self.__a, 'b = ', self.__b)

a1 = A(10,20)
a1.myprint()

a1(80)
```
答案： 为了能让对象实例能被直接调用，需要实现`__all__`方法
```
class A(object):
    def __init__(self, a, b):
        self.__a = a
        self.__b = b
    
    def myprint(self):
        print('a = ', self.__a, 'b = ', self.__b)
    
    def __call__(self, num):
        print('call:', num + self.__a)
```
