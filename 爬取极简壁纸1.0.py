import requests
from bs4 import BeautifulSoup
import json
import re
import os
 
base_url= 'https://w.wallhaven.cc/full/'
novel_save_dir= os.path.join(os.path.abspath(os.path.dirname(__file__)),'极简壁纸/')
print('当前执行的脚本文件路径为'+ os.path.abspath(__file__))
print('壁纸下载的文件夹路径为' + os.path.abspath(os.path.dirname(__file__)) + '/极简壁纸')
img_name =''
img_type =''
count= 1
 
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
        img_type = img[0]
        img_name = img[2]
        if img_type == 'j': # 判断图片格式
            url = base_url + img_name[0:2] + '/wallhaven-' + img_name + '.jpg'
            img_type = '.jpg'
            download_img(url,img_name,img_type)
        else:
            url = base_url + img_name[0:2] + '/wallhaven-' + img_name + '.png'
            img_type = '.png'
            download_img(url,img_name,img_type)
            
def download_img(url,img_name,img_type):
    try:
        headers= {
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69'
            }
        img= requests.get(url,headers=headers)
        with open(novel_save_dir + img_name + img_type ,'wb+')as f:
            f.write(img.content)
    except:
        print('')
    else:
        print('下载完成:' + img_name)
 
 
if __name__ == "__main__":
    if not os.path.exists(novel_save_dir): # 判断文件夹是否存在，不存在则创建
        os.mkdir(novel_save_dir)
    for count in range(1,10):
        get_data(count)