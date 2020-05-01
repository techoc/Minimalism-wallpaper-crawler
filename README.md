# Minimalism-wallpaper-crawler
爬取https://bz.zzzmh.cn/极简壁纸
具体实现可以查看博客:
1. 1.0版本：https://www.techoc.cn/index.php/archives/227/ 
2. 2.0版本：https://www.techoc.cn/index.php/archives/229/ 实现多线程爬取
3. 2.1版本：https://www.techoc.cn/index.php/archives/226/ 实现多进程爬取

# 需要用到的库：
requests
BeautifulSoup
gevent

# 注意：
### 由于`wallhaven`在中国并不稳定的原因，该脚本可能会长时间无法结束，手动结束即可。
1. 在2020年4月21日之前，极简壁纸是通过链接`wallhaven`的图片进行下载的。而在这之后极简壁纸开启cdn，由于是小众网站，所以cdn服务较为昂贵。
2. 本脚本解析出来的极简壁纸图片链接是`wallhaven`的图片链接，所以并不大量消耗极简壁纸的服务器资源。
3. 希望极简壁纸的作者撑住，也希望大家看到这个库的时候，极简壁纸还能存在。
