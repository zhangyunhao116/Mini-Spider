# Mini-Spider

[![PyPI](https://img.shields.io/pypi/v/yagmail.svg?style=flat-square)](https://pypi.python.org/pypi/mini-spider/)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)](https://pypi.python.org/pypi/mini-spider/)

mini-spider是一个简单、易用的爬虫工具，它可以帮助你迅速的爬取你想要提取的内容，而不需要关注诸如正则表达式、网络环境、下载器等一系列烦人的事情。

使用mini-spider，你仅需要四步即可创建属于你自己的爬虫！（大部分时候）

```console
$ mini-spider -a http://www.fengniao.com jpg html
[0]:
---(0)http://icon.fengniao.com/index/2016/images/jiaoquan/qrcode-b.jpg
---(1)http://icon.fengniao.com/index/2016/images/jiaoquan/qrcode-bk.jpg
---(2)http://icon.fengniao.com/index/images/qrcode-weixin.jpg
...
[1]:
---(0)http://pic.fengniao.com/201703/fn3876hp760400_0323.jpg
[2]:
---(0)http://2.fengniao.com/price/0-0-0-0-12-0-def-1_1.html
---(1)http://2.fengniao.com/price/0-0-0-0-15-0-def-1_1.html
---(2)http://2.fengniao.com/price/0-0-0-0-2-0-def-1_1.html
---(3)http://2.fengniao.com/price/0-0-0-0-24-0-def-1_1.html
---(4)http://2.fengniao.com/price/0-0-0-0-26-0-def-1_1.html
---(5)http://2.fengniao.com/price/0-0-0-0-3-0-def-1_1.html
...
[3]:
---(0)http://qsy.fengniao.com/534/5343356.html
---(1)http://qsy.fengniao.com/534/5343423.html
---(2)http://qsy.fengniao.com/534/5343457.html
---(3)http://sai.fengniao.com/topic/5339077.html
---(4)http://travel.fengniao.com/533/5339985.html
...
$ mini-spider -c 1 -to r
$ mini-spider -c 3 -to u
$ mini-spider -start
url: 19/19||resource: 9/9
...
url: 0/19||resource: 289/289
$ mini-spider -download /User/zyh/test
```

## 安装

安装前注意：

- 只依赖于python 3.x ，不兼容pyhon 2.x


- 本项目不需要任何第三方依赖。

 下载整个项目，切换到本目录，在终端中执行

```console
$ python3 setup.py install
```

或者，使用pip下载

```console
$ pip install mini-spider
```

## 使用

#### **1.首先你需要分析一个网站，并输入你想提取的内容（包含下一个网站的地址和你需要的资源），如**

```
$ mini-spider -a http://www.fengniao.com jpg html
```

***-a*** 命令:

分析网站从而创建相应的提取器，第一个参数为必要参数，即你需要分析的网站地址，后面紧接着你所需要的资源，诸如html、jpg、doc、mp3等所有你需要的资源。

然后mini-spider会输出所有可以匹配的资源并打印到终端。

#### **2.查看相应的匹配项，创建你所需要的提取器。如**

```console
$ mini-spider -c 0 1 3 -to u
```

 ***-c*** 命令:

选择你所需要创建提取器的项，命令最多需要3个参数，第一个为总的块索引，后两个参数为项的范围。第一个参数为必要参数，如果

- 如果只提供第一个参数，则选择该块所有项来创建提取器。
- 如果提供两个参数，则选择该块的某一项来创建提取器。
- 如果提供三个参数，则选择该块的一个范围内的项来创建提取器，这个范围是[第二个参数，第三个参数]，闭区间。若第二个参数和第三个参数相等，则此时仅有一个参数参与创建提取器。

***-to*** 命令:

仅在 ***-c*** 命令出现时使用，作用为选择该提取器输出内容是属于什么内容。mini-spider仅提供两种选项，即u(URL,网址)和r(resource,资源)

#### **3.启动爬虫，爬取相应的网址和资源。**

```console
$ mini-spider -start http://www.fengniao.com
```

***-start*** 命令:

启动爬虫，指定的第一个参数为爬虫第一个爬取的原始地址。

其可以不指定参数，此时如果在数据库中没有url可以提供，爬虫将不会运行。

#### **4.下载数据库中相应的资源。**

```console
$ mini-spider -download /User/zyh/test
```

***-download*** 命令:

启动下载器下载所需要的内容。可选参数为下载的绝对路径，如果未指定使用当前终端所在目录。

- 每个来自不同URL的提取资源会自动存放在目录中不同的文件夹
- 下载器有断点续传功能，文件未下载成功，重新运行本命令即可

## 当前版本

Ver 0.0.1 : 基本功能测试阶段。
