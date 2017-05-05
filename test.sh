#! /bin/bash
python3 mini-spider -a http://bbs.fengniao.com/forum/9373824.html jpg html
python3 mini-spider -c 0 -to r
python3 mini-spider -c 11 2 -to u
python3 mini-spider -start http://bbs.fengniao.com/forum/9373824.html
python3 mini-spider -download heretestdownload -false