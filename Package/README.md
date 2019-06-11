## 1.python包的导入——\_\_init\_\_.py
  Python中常见的文件导入模式：事先写好一个.py文件，如果在另一个.py文件中需要导入事先写好的.py文件时，就将事先写好的.py文件拷贝到当前目录，或者是
sys.path增加事先写好的.py文件所在的目录，然后import。这种做法对于少数文件是可行的，但如果程序数目多，层级复杂，就不适用。鉴于此，我们希望找到一种
办法，像Java的Package一样，能将多个.py文件组织起来，以实现在外部统一调用和在内部互相调用。
***
  其实，主要是用到Python的包的概念，而\_\_init\_\_.py在包里起着重要作用。要弄明白这个问题，首先要知道，Python在执行import语句时，到底进行了什么操作，按
照python的文档，它执行了如下操作：

1. 创建一个新的，空的module对象（它可能包含多个module）
2. 把这个module对象插入sys.module中
3. 装载module的代码（如果需要，首先必须编译）
4. 执行新的module中对应的代码。

  在执行第3步时，首先要找到module程序所在的位置。其原理为：如果需要导入的module的名字是m1，则解释器必须找到m1.py，它首先在当前目录查找，然后是在环境
变量PYTHONPATH中查找。PYTHONPATH可以视为系统的PATH变量一类的东西，其中包含若干个目录。如果PYTHONPATH没有设定，或者找不到m1.py，则继续搜索与Python
的安装设置相关的默认路径。正因为存在这样的顺序，如果当前路径或PYTHONPATH中存在与标准module同样的module，则会覆盖标准module。也就是说，如果当前目录下
存在xml.py，那么执行import xml时，导入的是当前目录下的module，而不是系统标准的xml。
***
  了解了这些，我们就可以先构建一个package，以普通module的方式导入，就可以直接访问此package中的各个module了。Python中的package定义很简单，其层次结构
与程序所在目录的层次结构相同，这一点与Java类似，唯一不同的地方在于，python中的package必须包含一个\_\_init\_\_.py的文件。
例如，我们可以这样组织一个package:
```
package1/
    __init__.py
    subPack1/
        __init__.py
        module_11.py
        module_12.py
        module_13.py
    subPack2/
        __init__.py
        module_21.py
        module_22.py
    ……
```

\_\_init\_\_.py可以为空，只要它存在，就表明此目录应被作为一个package处理。当然，\_\_init\_\_.py中也可以设置相应的内容，下文详细介绍。好了，现在我们在
module_11.py中定义一个函数：
```
def funA():
    print "funcA in module_11"
    return
```

在顶层目录（也就是package1所在的目录，当然也参考上面的介绍，将package1放在解释器能够搜索到的地方）运行python:
```
>>>from package1.subPack1.module_11 import funcA
>>>funcA()
funcA in module_11
```
这样，我们就按照package的层次关系，正确调用了module_11中的函数。
心的用户会发现，有时在import语句中会出现通配符*，导入某个module中的所有元素，这是怎么实现的呢？
答案就在\_\_init\_\_.py中。我们在subPack1的\_\_init\_\_.py文件中写\_\_all\_\_ = ['module\_13', 'module\_12'] ,然后进入python
```
>>>from package1.subPack1 import *
>>>module_11.funcA()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named module_11
```
也就是说，以*导入时，package内的module是受\_\_init\_\_.py限制的。
好了，最后来看看，如何在package内部互相调用。如果希望调用同一个package中的module，则直接import即可。也就是说，在module\_12.py中，可以直接使用
`import module_11`
如果不在同一个package中，例如我们希望在module\_21.py中调用module\_11.py中的FuncA，则应该这样：`from module_11包名.module_11 import funcA`

## 2.Python打包分发工具setuptools简介
---
作为Python标准的打包及分发工具，setuptools可以说相当地简单易用。它会随着Python一起安装在你的机器上。你只需写一个简短的setup.py安装文件，就可以
将你的Python应用打包。本文就会介绍下如何编写安装文件及如何打包分发。

首先，如果你需要另外安装setuptools，你可以使用下面的命令：
```
wget http://peak.telecommunity.com/dist/ez_setup.py
sudo python ez_setup.py
```
### 2.1.第一个安装文件
接下来让我们编写安装文件，假设我们的项目名为setup-demo，包名为myapp，目录结构如下：
```
setup-demo/
  ├ setup.py         # 安装文件
  └ myapp/           # 源代码
      ├ __init__.py    
      ...
```

一个最基本的setup.py文件如下：
```
#coding:utf8
from setuptools import setup
 
setup(
    name='MyApp',         # 应用名
    version='1.0',        # 版本号
    packages=['myapp']    # 包括在安装包内的Python包
)
```

### 2.2.执行安装文件
有了上面的setup.py文件，我们就可以打各种包，也可以将应用安装在本地Python环境中。
#### 2.2.1.创建egg包
```
python setup.py bdist_egg
```
该命令会在当前目录下的”dist”目录内创建一个egg文件，名为”MyApp-1.0-py2.7.egg”。文件名格式就是”应用名-版本号-Python版本.egg”，我本地Python版本是2.7。同时你会注意到，当前目录多了”build”和”MyApp.egg-info”子目录来存放打包的中间结果。
#### 2.2.2.创建tar.gz包
```
python setup.py sdist --formats=gztar
```
同上例类似，只不过创建的文件类型是tar.gz，文件名为”MyApp-1.0.tar.gz”。

#### 2.2.3.安装应用
```
python setup.py install
```
该命令会将当前的Python应用安装到当前Python环境的”site-packages”目录下，这样其他程序就可以像导入标准库一样导入该应用的代码了。
#### 2.2.4.开发方式安装
```
python setup.py develop
```
如果应用在开发过程中会频繁变更，每次安装还需要先将原来的版本卸掉，很麻烦。使用”develop”开发方式安装的话，应用代码不会真的被拷贝到本地Python环境的”site-packages”目录下，而是在”site-packages”目录里创建一个指向当前应用位置的链接。这样如果当前位置的源码被改动，就会马上反映到”site-packages”里。

### 2.3.引入非Python文件
上例中，我们只会将”myapp”包下的源码打包，如果我们还想将其他非Python文件也打包，比如静态文件（JS，CSS，图片），应该怎么做呢？这时我们要在项目目录下添加一个”MANIFEST.in”文件夹。假设我们把所有静态文件都放在”static”子目录下，现在的项目结构如下：
```
setup-demo/
  ├ setup.py         # 安装文件
  ├ MANIFEST.in      # 清单文件
  └ myapp/           # 源代码
      ├ static/      # 静态文件目录    
      ├ __init__.py    
      ...
```
我们在清单文件”MANIFEST.in”中，列出想要在包内引入的目录路径：
```
recursive-include myapp/static *
recursive-include myapp/xxx *
```
“recursive-include”表明包含子目录。别急，还有一件事要做，就是在”setup.py”中将” include_package_data”参数设为True：
```
#coding:utf8
from setuptools import setup
 
setup(
    name='MyApp',         # 应用名
    version='1.0',        # 版本号
    packages=['myapp'],   # 包括在安装包内的Python包
    include_package_data=True    # 启用清单文件MANIFEST.in
)
```
之后再次打包或者安装，”myapp/static”目录下的所有文件都会被包含在内。如果你想排除一部分文件，可以在setup.py中使用”exclude_package_date”参数，比如
```
setup(
    ...
    include_package_data=True,    # 启用清单文件MANIFEST.in
    exclude_package_date={'':['.gitignore']}
)
```
上面的代码会将所有”.gitignore”文件排除在包外。如果上述”exclude_package_date”对象属性不为空，比如”{‘myapp’:[‘.gitignore’]}”，就表明只排除”myapp”包下的所有”.gitignore”文件

### 2.4.自动安装依赖
我们的应用会依赖于第三方的Python包，虽然可以在说明文件中要求用户提前安装依赖包，但毕竟很麻烦，用户还有可能装错版本。其实我们可以在setup.py文件中指定依赖包，然后在使用setuptools安装应用时，依赖包的相应版本就会被自动安装。让我们来修改上例中的setup.py文件，加入”install_requires”参数：
```
#coding:utf8
from setuptools import setup
 
setup(
    name='MyApp',         # 应用名
    version='1.0',        # 版本号
    packages=['myapp'],   # 包括在安装包内的Python包
    include_package_data=True,    # 启用清单文件MANIFEST.in
    exclude_package_date={'':['.gitignore']},
    install_requires=[    # 依赖列表
        'Flask>=0.10',
        'Flask-SQLAlchemy>=1.5,<=2.1'
    ]
)
```
上面的代码中，我们声明了应用依赖Flask 0.10及以上版本，和Flask-SQLAlchemy 1.5及以上、2.1及以下版本。setuptools会先检查本地有没有符合要求的依赖包，如果没有的话，就会从PyPI中获得一个符合条件的最新的包安装到本地。
大家可以执行下试试，你会发现不但Flask 0.10.1（当前最新版本）被自动安装了，连Flask的依赖包Jinja2和Werkzeug也被自动安装了，很方便吧。
如果应用依赖的包无法从PyPI中获取怎么办，我们需要指定其下载路径：
```
setup(
    ...
    install_requires=[    # 依赖列表
        'Flask>=0.10',
        'Flask-SQLAlchemy>=1.5,<=2.1'
    ],
    dependency_links=[    # 依赖包下载路径
        'http://example.com/dependency.tar.gz'
    ]
)
```
路径应指向一个egg包或tar.gz包，也可以是个包含下载地址（一个egg包或tar.gz包）的页面。个人建议直接指向文件。

### 2.5.自动搜索Python包
之前我们在setup.py中指定了”packages=[‘myapp’]”，说明将Python包”myapp”下的源码打包。如果我们的应用很大，Python包很多怎么办。大家看到这个参数是一个列表，我们当然可以将所有的源码包都列在里面，但肯定很多人觉得这样做很傻。的确，setuptools提供了”find_packages()”方法来自动搜索可以引入的Python包：
```
#coding:utf8
from setuptools import setup, find_packages
 
setup(
    name='MyApp',               # 应用名
    version='1.0',              # 版本号
    packages=find_packages(),   # 包括在安装包内的Python包
    include_package_data=True,   # 启用清单文件MANIFEST.in
    exclude_package_date={'':['.gitignore']},
    install_requires=[          # 依赖列表
        'Flask>=0.10',
        'Flask-SQLAlchemy>=1.5,<=2.1'
    ]
)
```
这样当前项目内所有的Python包都会自动被搜索到并引入到打好的包内。”find_packages()”方法可以限定你要搜索的路径，比如使用”find_packages(‘src’)”就表明只在”src”子目录下搜索所有的Python包。

### 2.6.补充
* zip_safe参数
决定应用是否作为一个zip压缩后的egg文件安装在当前Python环境中，还是作为一个以.egg结尾的目录安装在当前环境中。因为有些工具不支持zip压缩文件，而且压缩后的包也不方便调试，所以建议将其设为False：”zip_safe=False”。
* 描述信息
部分参数提供了更多当前应用的细节信息，对打包安装并无任何影响，比如：
```
setup(
    ...
    author = "Billy He",
    author_email = "billy@bjhee.com",
    description = "This is a sample package",
    license = "MIT",
    keywords = "hello world example",
    url = "http://example.com/HelloWorld/",   # 项目主页
    long_description=__doc__,   # 从代码中获取文档注释
)
```
