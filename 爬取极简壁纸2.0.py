import gevent 
from gevent import monkey   # 从gevent库里导入monkey模块。
monkey.patch_all()
# 把import gevent，from gevent import monkey，monkey.patch_all()三行语句放在其他所有的import语句之前，可以避免出现警告或者报错信息
from gevent.queue import Queue  # 从gevent库里导入queue模块
from bs4 import BeautifulSoup
import requests,os,re,json,time
 
base_url= 'https://w.wallhaven.cc/full/'
novel_save_dir= os.path.join(os.path.abspath(os.path.dirname(__file__)),'极简壁纸/')
print('当前执行的脚本文件路径为'+ os.path.abspath(__file__))
print('壁纸下载的文件夹路径为' + os.path.abspath(os.path.dirname(__file__)) + '/极简壁纸')
img_name =''
img_type =''
url_list = []
work = Queue()  # 创建队列对象，并赋值给work。
tasks_list  = []   # 创建空的任务列表
start = time.time()
 
def add_url_work():
    for url in url_list:
        work.put_nowait(url)
 
def get_img_queue():
    while not work.empty(): # 当队列不是空的时候，就执行下面的程序。
        url = work.get_nowait() # 用get_nowait()函数可以把队列里的网址都取出。
        download_img(url)
        print(url,work.qsize())   # 打印网址、队列长度、抓取请求的状态码。
 
def get_data(count):
    url = 'https://api.zzzmh.cn/bz/getJson'
    headers= {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "access": "3111c568d1242b689b9a0380dc2ca665549ef1416b0864a1cd72010c94e94ddc",
    "content-length": "30",
    "content-type": "application/json",
    "location": "bz.zzzmh.cn",
    "origin": "https",
    "referer": "https",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sign": "error",
    "timestamp": "1585389526757",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69"
}
    data = {
        'target': "anime",
        'pageNum': count
    }
    res = requests.post(url,data=json.dumps(data),headers=headers)
    img_re = re.findall('"t":"([j,p])","x":(.*?),"i":"(.*?)"',res.text)
    for img in img_re:
        img_name = img[2]
        img_type = img[0]
        if img_type == 'j':
            url = base_url + img_name[0:2] + '/wallhaven-' + img_name + '.jpg'
            url_list.append(url)
        else:
            url = base_url + img_name[0:2] + '/wallhaven-' + img_name + '.png'
            url_list.append(url)
    add_url_work()
    
            
def download_img(url):
    try:
        headers= {
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69'
            }
        img= requests.get(url,headers=headers)
        img.raise_for_status()
        img_type = url.split('.')[-1]
        img_name = url.split('-')[-1]
        img_name = img_name.split('.')[0]
        with open(novel_save_dir + img_name + '.' + img_type ,'wb+')as f:
            f.write(img.content)
    except:
        print('')
 
def url_spawn():
    for x in range(32):  # 创建32个线程
            task = gevent.spawn(get_img_queue)  # 用gevent.spawn()函数创建执行crawler()函数的任务。
            tasks_list.append(task) # 往任务列表添加任务。
    gevent.joinall(tasks_list)  # 用gevent.joinall方法，执行任务列表里的所有任务，就是让爬虫开始爬取网站。
 
def mian():
    if not os.path.exists(novel_save_dir): # 判断文件夹是否存在，不存在则创建
        os.mkdir(novel_save_dir)
    for count in range(1,5): #爬取一页，一页有120张图片
        get_data(count)
    url_spawn()
    end = time.time()
    times = end-start
    print('本次爬取用时：'+ str(times) +'s')
 
if __name__ == "__main__":
    mian()