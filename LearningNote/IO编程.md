[TOC]

## 一、文件读写
所有文件进行读写前都需要通过`open()`函数打开，其函数原形如下：
```
open`(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)
```

### 1.1 读文件

标示符'r'表示读，如果文件不存在，`open()`函数就会抛出一个`IOError`的错误，并且给出错误码和详细的信息告诉你文件不存在：

```python
>>> f = open('/Users/michael/test.txt', 'r')
```

```python
>>> f=open('/Users/michael/notfound.txt', 'r')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
FileNotFoundError: [Errno 2] No such file or directory: '/Users/michael/notfound.txt'
```

如果文件打开成功，接下来，调用`read()`方法可以一次读取文件的全部内容，Python把内容读到内存，用一个`str`对象表示：

```python
>>> f.read()
'Hello, world!'
```

最后一步是调用`close()`方法关闭文件。文件使用完毕后必须关闭，因为文件对象会占用操作系统的资源，并且操作系统同一时间能打开的文件数量也是有限的：

```python
>>> f.close()
```

由于文件读写时都有可能产生`IOError`，一旦出错，后面的`f.close()`就不会调用。所以，为了保证无论是否出错都能正确地关闭文件，我们可以使用`try ... finally`或者`with`语句（`with`可以自动调用`close()`方法）来实现：

```python
try:
    f = open('/path/to/file', 'r')
    print(f.read())
finally:
    if f:
        f.close()
```

```python
with open('/path/to/file', 'r') as f:
    print(f.read())
```

调用`read()`会一次性读取文件的全部内容，若文件内容过大，可以采用反复调用`read(size)`（最多读取size个字节的内容，适合不确定文件大小）或者`readlines()`（每次读取一行内容，适合配置文件）：

```python
for line in f.readlines():
    print(line.strip()) # 把末尾的'\n'删掉
```



- file-like Object

  像`open()`函数返回的这种有个`read()`方法的对象，在Python中统称为file-like Object。除了file外，还可以是内存的字节流，网络流，自定义流等等。file-like Object不要求从特定类继承，只要写个`read()`方法就行。

  

- 读二进制文件

  要读取二进制文件，比如图片、视频等等，用`'rb'`模式打开文件即可：

```python
>>> f = open('/Users/michael/test.jpg', 'rb')
>>> f.read()
b'\xff\xd8\xff\xe1\x00\x18Exif\x00\x00...' # 十六进制表示的字节
```



- 读字符编码

  要读取非UTF-8编码的文本文件，需要给`open()`函数传入`encoding`参数，例如，读取GBK编码的文件：

```python
>>> f = open('/Users/michael/gbk.txt', 'r', encoding='gbk')
>>> f.read()
'测试'
```

遇到有些编码不规范的文件，你可能会遇到`UnicodeDecodeError`，因为在文本文件中可能夹杂了一些非法编码的字符。遇到这种情况，`open()`函数还接收一个`errors`参数，表示如果遇到编码错误后如何处理。最简单的方式是直接忽略：

```python
>>> f = open('/Users/michael/gbk.txt', 'r', encoding='gbk', errors='ignore')
```



### 1.2 写文件

写文件和读文件是一样的，唯一区别是调用`open()`函数时，传入标识符`'w'`或者`'wb'`表示写文本文件或写二进制文件：

```python
>>> f = open('/Users/michael/test.txt', 'w')
>>> f.write('Hello, world!')
>>> f.close()
```

**注意**

调用`write()`写入文件时，操作系统往往不会立刻把数据写入磁盘，而是放到内存缓存起来，空闲的时候再慢慢写入，只有调用`close()`方法时，操作系统才保证把没有写入的数据全部写入磁盘。

通常情况下通过`with`语句保证写入有效：

```python
with open('/Users/michael/test.txt', 'w') as f:
    f.write('Hello, world!')
```

要写入特定编码的文本文件，需要传入`encoding`参数，将字符串自动转换成指定编码。以`'w'`模式写入文件时，如果文件已存在，会直接覆盖（相当于删掉后新写入一个文件），若想以追加（append）模式写入，可传入`a`，具体参数看补充。



### 1.3 补充

- open模式

| Character | Meaning                                                      |
| --------- | ------------------------------------------------------------ |
| r         | 只读模式打开（默认）                                         |
| w         | 只写模式打开，若文件不存在则新建                             |
| x         | open for exclusive creation, failing if the file already exists |
| a         | 以追加模式打开 (从 EOF 开始, 必要时创建新文件)               |
| b         | 二进制模式                                                   |
| t         | 文本模式 (默认)                                              |
| +         | 以更新模式打开，可读可写                                     |
| r+        | 以读写模式打开                                               |
| w+        | 以读写模式打开 (参见 w )                                     |
| a+        | 以读写模式打开 (参见 a )                                     |
| rb        | 以二进制读模式打开                                           |
| wb        | 以二进制写模式打开 (参见 w )                                 |
| ab        | 以二进制追加模式打开 (参见 a )                               |
| rb+       | 以二进制读写模式打开 (参见 r+ )                              |
| wb+       | 以二进制读写模式打开 (参见 w+ )                              |
| ab+       | 以二进制读写模式打开 (参见 a+ )                              |



## 二、内存读写

### 2.1 StringIO

StringIO是在内存中读写`str`。

要把str写入StringIO，我们需要先创建一个StringIO，然后，像文件一样写入即可，写入完成后可通过`getvalue()`方法用于获得写入后的str。

```python
>>> from io import StringIO
>>> f = StringIO()
>>> f.write('hello')
5
>>> f.write(' ')
1
>>> f.write('world!')
6
>>> print(f.getvalue())
hello world!
```

StringIO的读取可以采用文件读取的类似方法

```python
>>> from io import StringIO
>>> f = StringIO('Hello!\nHi!\nGoodbye!')
>>> while True:
...     s = f.readline()
...     if s == '':
...         break
...     print(s.strip())
...
Hello!
Hi!
Goodbye!

```

### 2.2 BytesIO

BytesIO是在内存中读写二进制数据。

下面为写入UTF-8编码的bytes：

```python
>>> from io import BytesIO
>>> f = BytesIO()
>>> f.write('中文'.encode('utf-8'))
6
>>> print(f.getvalue())
b'\xe4\xb8\xad\xe6\x96\x87'
```

和StringIO类似，可以用一个bytes初始化BytesIO，然后，像读文件一样读取：

```python
>>> from io import BytesIO
>>> f = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
>>> f.read()
b'\xe4\xb8\xad\xe6\x96\x87'
```

**注意**

若使用Python2，使用StringIO会报错，可用BytesIO代替StringIO使用。

``` python
from io import BytesIO as StringIO

```

## open a disk file for updating (reading and writing)三、操作文件和目录

Python内置的`os`模块可以用于调用操作系统提供的接口函数，实现文件和目录的操作。

### 3.1 系统信息

1. **基本信息**

```python
import os
os.name # 操作系统类型
os.uname() # 系统详细信息
```

2. **环境变量**

在操作系统中定义的环境变量，全部保存在`os.environ`这个变量中，可以直接查看。

要获取某个环境变量的值，可以调用`os.environ.get('key')`：

```python
>>> os.environ.get('PATH')
'/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/opt/X11/bin:/usr/local/mysql/bin'
>>> os.environ.get('x', 'default')
'default'
```



### 3.2 操作文件和目录

操作文件和目录的函数一部分放在`os`模块中，一部分放在`os.path`模块中，同时`shutil`模块提供了很多相关函数，可作为`os`模块补充。

1. **基本操作**

- 目录操作

```python
# 查看当前目录的绝对路径:
>>> os.path.abspath('.')
'/Users/michael'
# 在某个目录下创建一个新目录，首先把新目录的完整路径表示出来:
>>> os.path.join('/Users/michael', 'testdir')
'/Users/michael/testdir'
# 然后创建一个目录:
>>> os.mkdir('/Users/michael/testdir')
# 删掉一个目录:
>>> os.rmdir('/Users/michael/testdir')
```

- 文件操作

```python
# 对文件重命名:
>>> os.rename('test.txt', 'test.py')
# 删掉文件:
>>> os.remove('test.py')
```

`os`模块不支持文件复制操作，可通过新建写入代替，或者使用`shutil`模块提供的`copyfile()`的函数

``` python
# shutil.copyfile( src, dst)
>>> shutil.copyfile('test.txt','Documents/test.txt')
```

**注意**

通过`shutil`模块无法复制所有文件的元数据，即在POSIX平台上，文件的所有者和组以及访问控制列表都将丢失。



2. **路径操作**

路径合并使用`os.path.join()`函数，可以自动处理不同系统的路径分割号。

```python
>>> os.path.join('/Users/michael', 'testdir')
'/Users/michael/testdir'
```

拆分路径使用`os.path.split()`函数，这样可以把一个路径拆分为两部分，后一部分总是最后级别的目录或文件名。

```python
>>> os.path.split('/Users/michael/testdir/file.txt')
('/Users/michael/testdir', 'file.txt')
```

使用`os.path.splitext()`可以直接让你得到文件扩展名

```python
>>> os.path.splitext('/path/to/file.txt')
('/path/to/file', '.txt')
```

3. **例子**

获取当前目录下所有文件，`os.listdir()`获取当前路径下所有目录及文件

```python
>>> [x for x in os.listdir('.') if os.path.isdir(x)]
```

获取当前目录下所有`py`文件

```python
>>> [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py']
```



## 四、序列化

我们把变量从内存中变成可存储或传输的过程称之为序列化，在Python中叫pickling，在其他语言中也被称之为serialization，marshalling，flattening等等，都是一个意思。

序列化之后，就可以把序列化后的内容写入磁盘，或者通过网络传输到别的机器上。

反过来，把变量内容从序列化的对象重新读到内存里称之为反序列化，即unpickling。

### 4.1 pickle

Python提供了`pickle`模块来实现序列化。

- 对象实例化后写入文件

```python
>>> import pickle
>>> d = dict(name='Bob', age=20, score=88)
>>> pickle.dumps(d)open a disk file for updating (reading and writing)

b'\x80\x03}q\x00(X\x03\x00\x00\x00ageq\x01K\x14X\x05\x00\x00\x00scoreq\x02KXX\x04\x00\x00\x00nameq\x03X\x03\x00\x00\x00Bobq\x04u.'
```

`pickle.dumps()`方法把任意对象序列化成一个`bytes`，然后，就可以把这个`bytes`写入文件。或者用另一个方法`pickle.dump()`直接把对象序列化后写入一个file-like Object：

```python
>>> f = open('dump.txt', 'wb')
>>> pickle.dump(d, f)
>>> f.close()
```

- 从文件读入实例化后的对象

当我们要把对象从磁盘读到内存时，可以先把内容读到一个`bytes`，然后用`pickle.loads()`方法反序列化出对象，也可以直接用`pickle.load()`方法从一个`file-like Object`中直接反序列化出对象。

```python
>>> f = open('dump.txt', 'rb')
>>> d = pickle.load(f)
>>> f.close()
>>> d
{'age': 20, 'score': 88, 'name': 'Bob'}
```

**注意**

`pickle`模块的问题和所有其他编程语言特有的序列化问题一样，就是它只能用于Python，并且可能不同版本的Python彼此都不兼容，因此，只能用Pickle保存那些不重要的数据。



### 4.2 JSON

如果我们要在不同的编程语言之间传递对象，就必须把对象序列化为标准格式，比如XML，但更好的方法是序列化为JSON，因为JSON表示出来就是一个字符串，可以被所有语言读取，也可以方便地存储到磁盘或者通过网络传输。JSON不仅是标准格式，并且比XML更快，而且可以直接在Web页面中读取，非常方便。

JSON表示的对象就是标准的JavaScript语言的对象，JSON和Python内置的数据类型对应如下：

|  JSON类型  | Python类型 |
| :--------: | :--------- |
|     {}     | dict       |
|     []     | list       |
|  "string"  | str        |
|  1234.56   | int或float |
| true/false | True/False |
|    null    | None       |

- 写入

Python内置的`json`模块提供了非常完善的Python对象到`JSON`格式的转换。

```python
>>> import json
>>> d = dict(name='Bob', age=20, score=88)
>>> json.dumps(d)
'{"age": 20, "score": 88, "name": "Bob"}'
# 写入
>>> f = open('dump.txt', 'wb')
>>> json.dump(d, f)
>>> f.close()
```

`dumps()`方法返回一个`str`，内容就是标准的`JSON`。类似的，`dump()`方法可以直接把`JSON`写入一个`file-like Object`。

- 读出

要把`JSON`反序列化为Python对象，用`loads()`或者对应的`load()`方法，前者把`JSON`的字符串反序列化，后者从`file-like Object`中读取字符串并反序列化：

```python
>>> json_str = '{"age": 20, "score": 88, "name": "Bob"}'
>>> json.loads(json_str)
{'age': 20, 'score': 88, 'name': 'Bob'}
# 读入
>>> f = open('dump.txt', 'rb')
>>> d = json.load(f)
>>> f.close()
```

- 进阶

``` python
json.dumps(*obj*, ***, *skipkeys=False*, *ensure_ascii=True*, *check_circular=True*, *allow_nan=True*, *cls=None*, *indent=None*, *separators=None*, *default=None*, *sort_keys=False*, ***kw*)
```

默认情况下，`JSON`无法序列化`class`，需要设置相关参数。

可选参数`default`就是把任意一个对象变成一个可序列为`JSON`的对象，我们只需要为`class`(`Student`)专门写一个转换函数，再把函数传进去即可：

```python
def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }
```
这样，`Student`实例首先被`student2dict()`函数转换成`dict`，然后再被顺利序列化为`JSON`：
```python
import json

class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

s = Student('Bob', 20, 88)
print(json.dumps(s,default=student2dict))
```

若想把任意`class`的实例变为`dict`，可采用以下写法：

```python
print(json.dumps(s, default=lambda obj: obj.__dict__))
```

因为通常`class`的实例都有一个`__dict__`属性，它就是一个`dict`，用来存储实例变量。也有少数例外，比如定义了`__slots__`的class。

同样的道理，如果我们要把`JSON`反序列化为一个`Student`对象实例，`loads()`方法首先转换出一个`dict`对象，然后，我们传入的`object_hook`函数负责把`dict`转换为`Student`实例：

```python
def dict2student(d):
    return Student(d['name'], d['age'], d['score'])
```

运行结果如下：

```python
>>> json_str = '{"age": 20, "score": 88, "name": "Bob"}'
>>> print(json.loads(json_str, object_hook=dict2student))
<__main__.Student object at 0x10cd3c190>
```



## 参考

[IO编程](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431917715991ef1ebc19d15a4afdace1169a464eecc2000)