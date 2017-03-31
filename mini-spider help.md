| 命令        |     作用      |   参数    |                    说明                    |                    示例                    |
| :-------- | :---------: | :-----: | :--------------------------------------: | :--------------------------------------: |
| -h        |     帮助      |    无    |                 查看程序帮助文档                 |              mini-spider -h              |
| -a        |    分析URL    | [1,+oo] |                 分析相应的URL                 |        mini-spider -a [URL] html         |
| -st       |    设置相似度    |    1    |          分析URL时，可以选择合适的相似阈值进行分类          |    mini-spider -a [URL] html -st 0.7     |
| -c        | 选择合适的块创建提取器 |  [1,3]  |     分析完URL后，选择合适的块创建提取器。（-to为其必要选项）      |        mini-spider -c 0 2 4 -to u        |
| -to       |  设置提取器数据流向  |    1    | 创建提取器时，设置提取器数据流向，参数只有两个选项u和r。分别代表流向URL数据库和资源数据库。 |        mini-spider -c 0 2 4 -to u        |
| -m        |   自定义提取器    |  [1,2]  | 使用自定义的正则表达式来创建提取器，可以添加Host值。（-to为其必要选项）  | mini-spider -m href="/\S+?.jpg" www.example.com -to u |
| -n        |    定义名称     |    1    |        可选命令，自定义提取器名称，不使用则由程序自动创建         | mini-spider -m href="/\S+?.jpg" www.example.com -to u -n my_url |
| -start    |    开始爬取     |  [0,1]  |       参数可选，为第一个爬取的URL，若不提供则从数据库中提取       |    mini-spider -start www.example.com    |
| -download |    开始下载     |  [0,1]  |        参数可选，自定义下载路径，若不指定则在当前目录下载         |   mini-spider -download /User/zyh/test   |
