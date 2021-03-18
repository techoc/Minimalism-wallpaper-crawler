import multiprocessing
from multiprocessing import Pool
import requests,os,re,json,time

base_url= 'https://w.wallhaven.cc/full/'
novel_save_dir= os.path.join(os.path.abspath(os.path.dirname(__file__)),'极简壁纸/')
img_name =''
img_type =''
url_list = []

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

def process(url,count):
    try:
        start_url = time.time()
        res = requests.get(url)
        img_type = url.split('.')[-1]
        img_name = url.split('-')[-1]
        img_name = img_name.split('.')[0]
        res.raise_for_status()
        with open( novel_save_dir+img_name + '.' + img_type ,'wb+')as f:
            f.write(res.content)
        end_url = time.time()
        print('下载成功{} 耗费时间:{} 队列:{}'.format(url,(end_url - start_url),count))
    except:
        print('图片下载失败')
    

if __name__ == '__main__':
    count = 0
    start = time.time()
    if not os.path.exists(novel_save_dir): # 判断文件夹是否存在，不存在则创建
        os.mkdir(novel_save_dir)
    print('当前执行的脚本文件路径为'+ os.path.abspath(__file__))
    print('壁纸下载的文件夹路径为' + os.path.abspath(os.path.dirname(__file__)) + '/极简壁纸')
    for count in range(1,20): 
        get_data(count)
    p = Pool(4) # 32进程爬取
    for url in url_list:
        count=count+1 
        p.apply_async(process, args=(url,count))     
    p.close()
    p.join()
    end = time.time()
    print('\n本次爬取所用时间为:{}秒'.format(end - start))
