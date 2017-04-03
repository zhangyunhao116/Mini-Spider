
# Mini-Spider教程

作者：ZhangYunHao

Mini-Spider是一个实用的爬虫工具，它的意义在于快速获得你所要的资源，而不用去关注诸如爬虫构造、数据存储、网络环境、语言实现等一系列的事情。现在你只需要简单的几个命令，就可以获得你需要的东西！


* CONTENTS
{:toc}

## 1.安装

Mini-Spider是一个跨平台的工具，它只依赖于python官方库，理论上，任何可以运行python3.x的机器都可以运行Mini-Spider。

### 1.1 安装python3.x

任何平台，请先安装[Python3.x下载](https://www.python.org/downloads/)

### 1.2 安装Mini-Spider

在安装了python3.x后，有两种方法安装Mini-Spider

- ##### 在github中安装最新版本的Mini-Spider(推荐)

打开[github-Mini-Spider](https://github.com/ZYunH/Mini-Spider)，点击右上角的‘’Clone or Download“,后选择"Download ZIP"。解压下载的ZIP文件后，切换到解压后的目录，执行

```console
$ python3 setup.py install
```

- 使用pip安装Mini-Spider

pip是python的一个包管理系统，可以让你便捷地管理系统上的python包。

安装python-pip(注意必须是python3.x版本的pip)：

Linux下

```console
$ sudo apt-get python3-pip
```
Mac OS、windows下，在第一步中使用官网安装的python3.x包自带pip

在终端或cmd中执行

```console
$ pip install mini-spider
```

注：mac中，若未安装pyenv，需将上述pip改为pip3，因为系统自带的pip版本只支持python2.x

## 2.快速入门

如果系统中安装了mini-spider，请在终端中输入如下命令来确认安装

```console
$ mini-spider
usage: mini-spider [OPTION]... [URL]...

MiniSpider makes it easy to create user-friendly spider.

optional arguments:
  -h, --help            show this help message and exit
  -a [URL] [[URL] ...]  Analysis a URL.
  -st [float]           Set similarity_threshold,default = 0.6
  -c [num] [[num] ...]  Choose block make extractor.
  -time [float]         Set timeout.(default: 2)
  -to [{u,r}]           Choose match data.(default: u)
  -n [name]             Name your extractor.it can be ignored.
  -start [URL]          Start spider to get url and resource.
  -download [Path]      Download all url from database.
  -m [RE] [[RE] ...]    Make extractor by user.
  -export [FileName]    Export url from database.
  -import [FileName]    Import url into database.
  -list  [ ...]         List url in url_list or resource.options: "u" or "r"
  -false []             Disable classification function in -download.
  -reset [{u,r}]        Reset database stats = 1.(default: u)
```

如果以上信息显示如上，则表示安装正确

### 2.1 分析网址

mini-spider的一个特色就是自动定位并将资源分类。例如，你发现某个论坛上的图片（jpg格式）非常喜欢，但是一个个将其复制特别麻烦...你可以这样做

```console
$ mini-spider -a http://bbs.fengniao.com/forum/9373824.html jpg
```

在终端中，将会得到以下输出

```console
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
[3]:
---(0)http://img2.fengniao.com/290_module_images/240/58dcaa2287f13.jpg
---(1)http://img2.fengniao.com/290_module_images/240/58dcaa3e3cf75.jpg
---
...
```

（限于篇幅，部分资源使用...代替)

如果你将块编号为[0]中的任意地址复制到浏览器打开，你将会得到你所需要的图片。是不是很方便？

==-a==命令作用的查找一个网址中你所需要资源，第一个参数为网站地址，后面接着你所需要的资源类型（例如jpg doc html，注意不能加逗号，如 ~~.jpg~~ 这会造成解析错误！）

> 你也可以尝试，在你所需分析的网址后面加上不同的文件类型，你将会得到更多的资源，但是为了避免输出信息太多，难以识别（比如加上后面加html jpg，你将会得到上百条的资源信息），最好的方式是每次是分析一种类型资源。
>

但是为了提取他们，我们需要更多的工作

### 2.2 创建提取器

通常，我们创建一个提取器是一件很麻烦的事情，特别对于一些新手们更是如此，你需要考虑正则表达式匹配、不断比对页面代码之类的事情。但是，在mini-spider下，你只需要简单的一个命令就可以创建提取器。

首先，观察上面的例子。你将会发现，处于资源块[0]中的图片，都是作者所发布的图片。你只需要在终端上输入

```console
$ mini-spider -c 0 -to r
http://bbs.qn.img-space.com/[a-z][0-9]/[A-Z][0-9][0-9]/[0-9][0-9]/[0-9][A-Z]/[A-Z][a-z]-\S+?\.jpg
The extractor was created successfully！
```

这条命令的意思是，选择资源块[0]中的所有资源信息创建提取器，提取后的信息放入资源数据库中。

==-c==指定你需要选择的资源块，有些时候，一个大的资源块并不完全符合你心中的愿望，可能会混入一些不需要的资源，你可以选择一个资源块的一部分来创建提取器。例如

```console
$ mini-spider -c 0 0 3 -to r
```

代表着选择块[0]中的0至3的资源（闭区间）来创建提取器。

```console
$ mini-spider -c 0 1 -to r
```

代表着选择块[0]中的1资源来创建提取器。

==-to==以及后面的参数指定了提取后的信息去向。该参数仅有两个可选参数'-to u'或'-to r'，分别代表了提取后的信息放入url数据库(即包含所有需要爬取的url的数据库)或放入资源数据库中。

现在，你已经可以正确的提取你所要的资源了，但是，稍等！

你还需要定义下一个你需要爬取的地址，否则你只能提取当前页面的资源。

很显然，你需要提取下一个页面的url来进行爬取。

现在让我们再来分析一下刚才的url，但是，此时的资源类型为html。我们在浏览器中，点击该论坛下一页，会发现它的地址是http://bbs.fengniao.com/forum/9373824_2.html。

输入

```console
$ mini-spider -a http://bbs.fengniao.com/forum/9373824.html html
```

输出的信息很多，但是我们会发现块[5]中的2号资源符合我们的预期。

```console
...
[5]:
---(0)http://bbs.fengniao.com/forum/2879928.html
---(1)http://bbs.fengniao.com/forum/9373824.html
---(2)http://bbs.fengniao.com/forum/9373824_2.html
---(3)http://bbs.fengniao.com/forum/forum_11.html
...
```

输入

```console
$ mini-spider -c 5 2 -to u
Host:http://bbs.fengniao.com
href="(/[a-z][a-z][a-z][a-z][a-z]/[0-9][0-9][0-9][0-9][0-9][0-9][0-9]_[0-9]\.html)"
The extractor was created successfully！
```

现在，我们获得了下个网址和相应资源的提取器，开始爬取吧！



### 2.3 开始爬取

这个步骤会不断读取url数据库的内容，然后提取相应的内容放入相应的数据库。

输入

```console
$ mini-spider -start http://bbs.fengniao.com/forum/9373824.html
url: 1/1||resource: 9/9
url: 1/2||resource: 19/19
url: 1/3||resource: 21/21
url: 1/4||resource: 21/21
url: 1/5||resource: 21/21
url: 1/6||resource: 21/21
url: 1/7||resource: 21/21
url: 1/8||resource: 21/21
url: 0/8||resource: 21/21
```

==-start==作用是开始爬取，从第一个url开始（即-start后面紧跟的网址）不断将相应数据放入数据库中。

屏幕上会不断输出此时数据库的信息，直到无法爬取时，程序会自动停止，一些错误信息也会输出在屏幕上。



### 2.4 启动下载器

从上个步骤中，我们可以知道数据库已经爬取得到了21个资源，并自动关闭。

输入

```console
$ mini-spider -download -false
Cg-77VggNSKISexrAAvLkt1pk-sAADfPgMOPsEAC8uq536.jpg completed            
Cg-40lggNLuITlKGAAaIKdnN16YAADfPAIfryoABohB596.jpg completed            
Cg-77VggNWmIVXTwAAP2OrqqXKIAADfPwG44UYAA_ZS536.jpg completed            
Cg-77VggNemIXgi7AAX2dyHXWx0AADfQAEwyIAABfaP695.jpg completed            
Cg-40lggNo2IdlT0AAiEl8en1M0AADfQQKQklQACISv087.jpg completed
...
```

==-download==作用是启动下载器下载所有资源，默认放置如当前目录。

==-false==作用是禁止下载器分类，如果没有这个命令，下载器会默认将所有资源依据提取他们的地址分类（即这些图片在不同的文件夹内），显然我们只需要所有图片，而不需要将他们依据不同的页面分开。

现在，你需要的所有图片已经在当前的目录下了！



## 3.内置命令

现在，就来具体地介绍所有的mini-spider的内置命令吧！







### 3.1 命令列表

| 命令        |       作用        |     参数     |                    说明                    | 示例                                       |
| :-------- | :-------------: | :--------: | :--------------------------------------: | :--------------------------------------- |
| -h        |       帮助        |     无      |                 查看程序帮助文档                 | mini-spider -h                           |
| -a        |      分析URL      |  [1,+oo]   |                 分析相应的URL                 | mini-spider -a [URL] html                |
| -st       |      设置相似度      |     1      |      分析URL时，可以选择合适的相似阈值进行分类，默认为0.6       | mini-spider -a [URL] html -st 0.7        |
| -time     |     设置等待时间      |     1      |         分析URL或下载时，设置等待时间，默认为2 秒          | mini-spider -a [URL] html -st 0.7 -time 3 |
| -c        |   选择合适的块创建提取器   |   [1,3]    |     分析完URL后，选择合适的块创建提取器。（-to为其必要选项）      | mini-spider -c 0 2 4 -to u               |
| -to       |     设置数据流向      |   {u,r}    | 设置数据流向，参数只有两个选项u和r。分别代表流向为URL数据库或资源数据库。  | mini-spider -c 0 2 4 -to u               |
| -m        |     自定义提取器      |   [1,2]    | 使用自定义的正则表达式来创建提取器，可以添加Host值。（-to为其必要选项）  | mini-spider -m href="/\S+?.jpg" www.example.com -to u |
| -n        |      定义名称       |     1      |        可选命令，自定义提取器名称，不使用则由程序自动创建         | mini-spider -m href="/\S+?.jpg" www.example.com -to u -n my_url |
| -start    |      开始爬取       |   [0,1]    |       参数可选，为第一个爬取的URL，若不提供则从数据库中提取       | mini-spider -start www.example.com       |
| -download |      开始下载       |   [0,1]    |        参数可选，自定义下载路径，若不指定则在当前目录下载         | mini-spider -download /User/zyh/test     |
| -export   | 从数据库中导出url至文本文件 | [filename] | 参数为文件名（必要）。（-to为其必要选项，指定了从资源数据库或url数据库中导出url) | mini-spider -export 1.txt -to u          |
| -import   | 从文本文件中导出url至数据库 | [filename] | 参数为文件名（必要）。（-to为其必要选项，指定了从文本文件提取的信息放入资源数据库或url数据库) | mini-spider -import 1.txt -to u          |
| -list     |   打印数据库中信息至屏幕   |   [1,2]    | 第一个参数为必要，可选项为{u,r}，即选择url数据库或资源数据库。第二个参数可选，设置最大打印数目。 | mini-spider -list u 5                    |
| -false    |       禁止        |     无      |               禁止数据库自动分类功能                | mini-spider -download /User/zyh/test -false |
| -reset    |     重置数据库状态     |   {u,r}    |    将某个数据库中的所有url状态重置为可用，在下次爬取时会使用它们。     | mini-spider -reset u                     |

以上是mini-spider所有命令，下面会根据它们使用的时机进行介绍。



### 3.2 分析网址

自动将网址中的所需资源分类是Mini-Spider一大特色。

- [x] 自动资源分类，提取href标签
- [x] 自定义相似度阈值
- [x] 自定义等待时间

示例:

```cons
$ mini-spider -a http://www.example.com html zip -st 0.8 -time 3
```

#### 3.2.1 必要命令

- ==-a==，第一个参数为必要参数，如示例中的http://www.example.com


> 尽量输入url的协议，如果不输入程序会自动补充协议为http，例如输入www.example.com会自动补充为http://www.example.com但是这种情况有时会出现协议错误。

第二个参数为必要参数，即所需提取的资源类型，你至少输入一个，如示例中的 html zip

这些参数紧接在网址之后，这些参数会在程序中解析为通用正则表达式，所以例如 ~~.html~~ 这样的输入会造成解析错误，所以使用者不要加入逗号。

> 注意保持所分析资源类型数量，如果一次性分析很多，输出信息的数量巨大会造成观察困难。



#### 3.2.2 可选命令

- ==-st==，仅有一个参数，为必要参数，如示例中的 0.8

这个参数可以指定资源分类的相似度阈值，默认为0.6

只有相似度大于这个值的一类资源才可以归为一个分类，一般不需要改变这个值。

> 一般来说，提高阈值，分的类就越多，反之亦然。

- ==-time==，仅有一个参数，为必要参数，如示例中的 3

这个参数可以指定分析网站时的等待时间，默认为2，单位为 秒



#### 3.2.3 其他

- 默认情况下，每一块最多显示100个资源，如果超过这个值，便会显示 xxx is not displayed.此时可以提高参数==-st==来得到更多的分类从而减少每一块资源的数目
- 此时，生成的信息会自动存储到一个名为mini-spider.temp的文件中，如果此时切换目录，下个环节中便不可以自动创建提取器（因为此时mini-spider.temp不在当前目录）




### 3.3 创建提取器

这个环节中，你可以使用两种方式来创建提取器。一种是程序自动创建，一种是自己编写正则表达式创建。提取器后缀名为.extractor ，用户可以任意移动。程序启动时会自动检测当前目录的所有提取器，每次提取的内容会被所有提取器提取。

> 实际上，mini-spider的提取器是由一个正则表达式，还有一些补充信息构成

- [x] 自动创建正则表达式
- [x] 自动提取href信息并补充host信息
- [x] 自定义提取器及host信息



#### 3.3.1 自动创建

示例：

```
$ mini-spider -c 0 3 6 -to u -n next_url
```

必要命令

- ==-c==，共有三个参数，第一个为必要参数，其后两个参数为可选。全部使用时如示例中的 -c 0 3 6

三个参数全部使用，-c 0 3 6 代表着选择[0]块的3至6号资源来创建提取器（包括3和6）

只使用两个参数，-c 0 3 代表着选择[0]块的3号资源来创建提取器

只使用一个参数，-c 0  代表着选择[0]块的全部资源来创建提取器

> 建议使用尽量多的资源来创建提取器，这样可以提取成功率会大大提高。仅只用一个资源创建提取器时，精度会大大提高，但是提取成功率会大大降低。使用者需要根据实际平衡。

- ==-u==，仅有一个参数，选择数据流向，为必要参数。只能在-to u 和 -to r 中选择，-to u 代表着流向url数据库(to url database)，-to r代表着流向资源数据库(to resource database)

可选命令

- ==-n==，仅有一个参数，指定提取器名称，为必要参数。该参数不可加后缀名，例如 ~~next_url.txt~~ 为错误

> 提取器名字会自动创建，程序启动时会自动检测当前目录的所有提取器，故其名字并不重要。此时创建的提取器会自动添加后缀名，即创建的文件名为next_url.extractor



#### 3.3.2 自定义创建

示例：

```
$ mini-spider -m href="(\s+?\.html)" http://www.example.com -to u -n next_url
```

必要命令

- ==-m==，共有两个参数，第一个参数为必要参数，第二个为可选参数。

第一个参数为正则表达式，它是构成提取器的核心

第二个参数为补充参数，此参数会自动加入提取后的资源前，组成完整的url。一般为Host，例如在href标签中的资源提取出来后需要加上Host才能构成完整的url

- ==-u==，仅有一个参数，选择数据流向，为必要参数。只有能在-to u 和 -to r 中选择，-to u 代表着流向url数据库(to url database)，-to r代表着流向资源数据库(to resource database)

可选命令

- ==-n==，仅有一个参数，指定提取器名称，为必要参数。该参数不可加后缀名，例如 ~~next_url.txt~~ 为错误

> 提取器名字会自动创建，程序启动时会自动检测当前目录的所有提取器，故其名字并不重要。此时创建的提取器会自动添加后缀名，即创建的文件名为next_url.extractor



### 3.4 启动爬虫程序

启动爬虫程序，来获取url内容，这一步并不下载资源，只是将获得的资源放入相应数据库。

- [x] 自动更新数据库状态
- [x] 错误检查，状态恢复
- [x] 自动停止



示例：

```
$ mini-spider -start http://www.example.com -time 3
```

#### 3.4.1 必要命令

- ==-start==，仅有一个参数，为可选参数。作用为启动爬虫程序，不断从数据库中弹出url进行分析，然后将信息传入所有提取器，提取后的信息进入相应的数据库。

参数指定了第一个爬取的url，如果不提供参数，则从数据库中弹出，如果数据库中没有可用url，则启动失败。



#### 3.4.2 可选命令

- ==-time==，仅有一个参数，为必要参数，如示例中的 3

这个参数可以指定分析网站时的等待时间，默认为2，单位为 秒



### 3.5 启动下载器

示例:

```
$ mini-spider -download /Users/zyh/test -false
```

- [x] 支持断点续传
- [x] 自动检查url，补充协议以及中文转义
- [x] 自动添加文件名
- [x] 自定义下载路径，自动分类
- [x] 支持ftp、http、https协议



#### 3.5.1 必要命令

- ==-download==，仅有一个参数，为可选参数。作用为启动下载器，不断从数据库中弹出资源url下载。

参数指定了下载目录，绝对路径。如果没有指定，则程序默认选择当前目录作为下载目录。



#### 3.5.2 可选命令

- ==-false==，无参数。作用是禁止下载器自动分类功能。

> 自动分类功能：下载器默认启用，作用是将从不同url提取出来的资源放入不同的文件夹。



#### 3.5.3 其他

- 每次下载不成功时，该 url的状态不会变为0，而是依然为1，继续等待下次下载


- 如果有错误导致下载不成功，重新运行即可，下载器有断点续传功能。



### 3.6 数据库功能

这一部分讲述文本文件与数据库之间的数据交换。数据库名为MiniSpider.db，单文件，可以自行移动。

- [x] 使用错误自动恢复状态
- [x] 自动建立和检查数据库状态
- [x] 支持与纯文本文件的导入导出



#### 3.6.1 数据库的导出

示例：

```
$ mini-spider -export 1.txt -to u
```

必要命令

- ==-export==，仅有一个参数，为必要参数。作用是导出数据库中的url放入文本文件中。

参数的作用是指定导出文件名，纯文本文件，尽量加入后缀名 .txt

- ==-u==，仅有一个参数，选择数据流向，为必要参数。只有能在-to u 和 -to r 中选择，-to u 代表着流向url数据库(to url database)，-to r代表着流向资源数据库(to resource database)

> -u参数选择了从资源数据库或是url数据库中导出

其他

- 导出的文本文件会在每条内容后加入换行符"\n"方便观察



#### 3.6.2 数据库的导入

示例：

```
$ mini-spider -import 1.txt -to u
```

必要命令

- ==-import==，仅有一个参数，为必要参数。作用是将文本文件中的数据放入数据库中。

参数的作用是指定导入文件名，纯文本文件，需加入后缀名 .txt

- ==-u==，仅有一个参数，选择数据流向，为必要参数。只能在-to u 和 -to r 中选择，-to u 代表着流向url数据库(to url database)，-to r代表着流向资源数据库(to resource database)

> -u参数选择导入url数据库或是资源数据库

其他

- 导入的文本文件必须每条内容后加入换行符"\n"，如此程序才能正确解析





#### 3.6.3 在终端中查看数据库内容

示例：

```
$ mini-spider -list u 10
```

必要命令

- ==-list==，有两个参数，第一个必要，第二个可选。作用是将数据库中打印到终端中。

第一个参数如同参数==-to==，作用是指定数据流，即从url数据库或是资源数据库打印。只能在u 和 r 中选择。

第二个参数可选，作用是选择最大打印数目，以免打印过多造成不便。



#### 3.6.4 刷新数据库资源状态

示例：

```
$ mini-spider -reset u
```

> 数据库中每个url都具有一个状态，如果未被使用，他们的状态为1，如果被使用则变为0。

必要命令

- ==-reset==，仅有一个参数，选择数据流向，为必要参数。只能在-reset u 和 -reset r 中选择，-reset u 代表着刷新url数据库所有url状态为1，-reset u 代表着刷新资源数据库所有url状态为1
