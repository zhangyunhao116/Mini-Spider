# Mini-Spider

[![PyPI](https://img.shields.io/pypi/v/yagmail.svg?style=flat-square)](https://pypi.python.org/pypi/mini-spider/)
[![platform](https://img.shields.io/badge/python-3.5-green.svg)]()
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)](https://pypi.python.org/pypi/mini-spider/)

Mini-Spider是一个实用的爬虫工具，它的意义在于快速获得你所要的资源，而不用去关注诸如爬虫构造、数据存储、网络环境、语言实现等一系列的事情。现在你只需要简单的几个命令，就可以创建一个爬虫，并完成你的任务！

使用mini-spider，你仅需要四步即可创建属于你自己的爬虫！（大部分时候）

## 特性

- [x] 网页自动提取资源并根据算法分类（包括完整url和所有html标签内容）
- [x] 根据资源自动生成提取器
- [x] 自定义提取器以及Host数据
- [x] 自动将提取内容加入相应数据库
- [x] 自动分类下载，断点续传
- [x] 数据库导入和导出

简单地说，你只需要几个命令就可以爬取你想要的资源！


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

## 如何使用

## [Mini-spider使用教程](http://pythonhosted.org/mini-spider)

## 示例

这里演示使用三个命令创建爬虫，后使用两个命令完成全部任务。

示例目标：提取[这里](http://bbs.fengniao.com/forum/9373824.html)作者发布的所有图片

![example](https://github.com/ZYunH/Mini-Spider/blob/master/example.gif)

## 当前版本

Ver 0.0.4 : 基本功能测试阶段。
