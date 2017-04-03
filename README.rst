Mini-Spider
===========

|image0| |image1| |image2|

Mini-Spider是一个实用的爬虫工具，它的意义在于快速获得你所要的资源，而不用去关注诸如爬虫构造、数据存储、网络环境、语言实现等一系列的事情。现在你只需要简单的几个命令，就可以获得你需要的东西！

使用mini-spider，你仅需要四步即可创建属于你自己的爬虫！（大部分时候）

特性
----

-  网页自动提取资源并根据算法分类（包括完整url和href标签内容）

-  根据资源自动生成提取器

-  自定义提取器以及Host数据

-  自动将提取内容加入相应数据库

-  自动分类下载，断点续传

-  数据库导入和导出

简单地说，你只需要几个命令就可以爬取你想要的资源！

安装
----

安装前注意：

-  只依赖于python 3.x ，不兼容pyhon 2.x

-  本项目不需要任何第三方依赖。

 下载整个项目，切换到本目录，在终端中执行

.. code:: console

    $ python3 setup.py install

或者，使用pip下载

.. code:: console

    $ pip install mini-spider

如何使用
--------

↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓猛戳↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

`Mini-spider使用教程 <http://iamzyh.com/collection/>`__
-------------------------------------------------------

快速入门
--------

示例：

.. code:: console

    $ mini-spider -a http://bbs.fengniao.com/forum/9373824.html jpg
    [0]:
    ---(0)http://bbs.qn.img-space.com/g3/M00/02/3E/Cg-40lggN4GIcjIsAAbtzNgksRcAADfQwP38xwABu3k334.jpg
    ---(1)http://bbs.qn.img-space.com/g3/M00/02/3E/Cg-40lggN8KIC5XmAAPNyGCOY3kAADfRAL7-zgAA83g069.jpg
    ...
    [1]:
    ---(0)http://icon.fengniao.com/forum/images/complain_close.jpg
    ---(1)http://icon.fengniao.com/index/2016/images/jiaoquan/qrcode-b.jpg
    ...
    [2]:
    ---(0)http://image3.fengniao.com/head/1185/80/1184655_0.jpg
    ---(1)http://image3.fengniao.com/head/129/80/128323_0.jpg
    ...
    $ mini-spider -c 0 -to r
    http://bbs.qn.img-space.com/[a-z][0-9]/[A-Z][0-9][0-9]/[0-9][0-9]/[0-9][A-Z]/[A-Z][a-z]-\S+?\.jpg
    The extractor was created successfully！
    $ mini-spider -c 5 2 -to u
    Host:http://bbs.fengniao.com
    href="(/[a-z][a-z][a-z][a-z][a-z]/[0-9][0-9][0-9][0-9][0-9][0-9][0-9]_[0-9]\.html)"
    The extractor was created successfully！
    $ mini-spider -start http://bbs.fengniao.com/forum/9373824.html
    url: 1/1||resource: 9/9
    url: 1/2||resource: 19/19
    url: 1/3||resource: 21/21
    url: 1/4||resource: 21/21
    $ mini-spider -download -false
    Cg-77VggNSKISexrAAvLkt1pk-sAADfPgMOPsEAC8uq536.jpg completed            
    Cg-40lggNLuITlKGAAaIKdnN16YAADfPAIfryoABohB596.jpg completed            
    Cg-77VggNWmIVXTwAAP2OrqqXKIAADfPwG44UYAA_ZS536.jpg completed            
    Cg-77VggNemIXgi7AAX2dyHXWx0AADfQAEwyIAABfaP695.jpg completed            
    Cg-40lggNo2IdlT0AAiEl8en1M0AADfQQKQklQACISv087.jpg completed
    ...

**1.首先你需要分析一个网站，并输入你想提取的内容（包含下一个网站的地址和你需要的资源），如**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: 

    $ mini-spider -a http://www.fengniao.com jpg html

***-a*** 命令:

分析网站从而创建相应的提取器，第一个参数为必要参数，即你需要分析的网站地址，后面紧接着你所需要的资源，诸如html、jpg、doc、mp3等所有你需要的资源。

然后mini-spider会输出所有可以匹配的资源并打印到终端。

**2.查看相应的匹配项，创建你所需要的提取器。如**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: console

    $ mini-spider -c 0 1 3 -to u

 ***-c*** 命令:

选择你所需要创建提取器的项，命令最多需要3个参数，第一个为总的块索引，后两个参数为项的范围。第一个参数为必要参数，如果

-  如果只提供第一个参数，则选择该块所有项来创建提取器。

-  如果提供两个参数，则选择该块的某一项来创建提取器。

-  如果提供三个参数，则选择该块的一个范围内的项来创建提取器，这个范围是[第二个参数，第三个参数]，闭区间。若第二个参数和第三个参数相等，则此时仅有一个参数参与创建提取器。

***-to*** 命令:

仅在 ***-c***
命令出现时使用，作用为选择该提取器输出内容是属于什么内容。mini-spider仅提供两种选项，即u(URL,网址)和r(resource,资源)

**3.启动爬虫，爬取相应的网址和资源。**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: console

    $ mini-spider -start http://www.fengniao.com

***-start*** 命令:

启动爬虫，指定的第一个参数为爬虫第一个爬取的原始地址。

其可以不指定参数，此时如果在数据库中没有url可以提供，爬虫将不会运行。

**4.下载数据库中相应的资源。**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: console

    $ mini-spider -download /User/zyh/test

***-download*** 命令:

启动下载器下载所需要的内容。可选参数为下载的绝对路径，如果未指定使用当前终端所在目录。

-  每个来自不同URL的提取资源会自动存放在目录中不同的文件夹

-  下载器有断点续传功能，文件未下载成功，重新运行本命令即可

当前版本
--------

Ver 0.0.2 : 基本功能测试阶段。

.. |image0| image:: https://img.shields.io/pypi/v/yagmail.svg?style=flat-square
   :target: https://pypi.python.org/pypi/mini-spider/
.. |image1| image:: https://img.shields.io/badge/python-3.5-green.svg
   :target: 
.. |image2| image:: https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square
   :target: https://pypi.python.org/pypi/mini-spider/
