# property()函数：定义属性
***
正常情况下的类，它包含的属性应该是隐藏的，只允许通过类提供的方法来间接实现对类属性的访问和操作
因此，在不破坏类封装原则的基础上，为了能够有效操作类中的属性，类中应包含读（或写）类属性的多个 getter（或 setter）方法，这样就可以通过“类对象.方法
(参数)”的方式操作属性，例如：
```
class Rectangle:
    # 定义构造方法
    def __init__(self, width, height):
        self.width = width
        self.height = height
    # 定义setsize()函数
    def setsize (self , size):
        self.width, self.height = size
    # 定义getsize()函数
    def getsize (self):
        return self.width, self.height
     # 定义delsize()函数
    def delsize (self):
        self.width, self.height = 0, 0
rect = Rectangle(3 , 4)
rect.setsize((6,8))
print(rect.getsize())
```
运行结果为：
```
(6,8)
```

这种操作类属性的方式比较麻烦，更习惯使用“类对象.属性”这种方式。庆幸的是，Python 中提供了property() 函数，可以实现在不破坏类封装原则的前提下，让
开发者依旧使用“类对象.属性”的方式操作类中的属性

property() 函数的基本使用格式如下：

    属性名=property(fget=None, fset=None, fdel=None, doc=None)

其中，fget 参数用于指定获取该属性值的类方法，fset 参数用于指定设置该属性值的方法，fdel 参数用于指定删除该属性值的方法，最后的 doc 是一个文档字符串，
用于提供说明此函数的作用
开发者调用 property() 函数时，可以传入 0 个（既不能读，也不能写的属性）、1 个（只读属性）、2 个（读写属性）、3 个（读写属性，也可删除）和 4 个（读写
属性，也可删除，包含文档说明）参数

例如，对前面的 Rectangle 类做适当的修改，使用 property() 函数定义一个 size 属性：
```
class Rectangle:
    # 定义构造方法
    def __init__(self, width, height):
        self.width = width
        self.height = height
    # 定义setsize()函数
    def setsize (self , size):
        self.width, self.height = size
    # 定义getsize()函数
    def getsize (self):
        return self.width, self.height
     # 定义getsize()函数
    def delsize (self):
        self.width, self.height = 0, 0 
    # 使用property定义属性
    size = property(getsize, setsize, delsize, '用于描述矩形大小的属性')
# 访问size属性的说明文档
print(Rectangle.size.__doc__)
# 通过内置的help()函数查看Rectangle.size的说明文档
help(Rectangle.size)
rect = Rectangle(4, 3)
# 访问rect的size属性
print(rect.size) # (4, 3)
# 对rect的size属性赋值
rect.size = 9, 7
# 访问rect的width、height实例变量
print(rect.width) # 9
print(rect.height) # 7
# 删除rect的size属性
del rect.size
# 访问rect的width、height实例变量
print(rect.width) # 0
print(rect.height) # 0
```
程序中，使用 property() 函数定义了一个 size 属性，在定义该属性时一共传入了 4 个参数，这意味着该属性可读、可写、可删除，也有说明文档。所以，该程序
尝试对 Rectangle 对象的 size 属性进行读、写、删除操作，其实这种读、写、删除操作分别被委托给 getsize()、setsize() 和 delsize() 方法来实现

运行上面程序，将会看到如下输出结果：
```
用于描述矩形大小的属性
Help on property:

    用于描述矩形大小的属性

(4, 3)
9
7
0
0
```

在使用 property() 函数定义属性时，也可根据需要只传入少量的参数。例如，如下代码使用 property() 函数定义了一个读写属性，该属性不能删除：
```
class User :
    def __init__ (self, first, last):
        self.first = first
        self.last = last
    def getfullname(self):
        return self.first + ',' + self.last
    def setfullname(self, fullname):
        first_last = fullname.rsplit(',');
        self.first = first_last[0]
        self.last = first_last[1]
    # 使用property()函数定义fullname属性，只传入2个参数
    # 该属性是一个读写属性，但不能删除
    fullname = property(getfullname, setfullname)
u = User('悟空', '孙')
# 访问fullname属性
print(u.fullname)
# 对fullname属性赋值
u.fullname = '八戒,朱'
print(u.first)
print(u.last)
```

此程序中使用 property() 定义了 fullname 属性，该程序使用 property() 函数时只传入两个参数，分别作为 getter 和 setter方法，因此该属性是一个读写
属性，不能删除
运行上面程序，将看到如下输出结果：
```
悟空,孙
八戒
朱
```
