# -*- encoding: utf-8 -*-
'''
@File    :   card_downloader.py
@Time    :   2021/01/25 20:26:35
@Author  :   Tang Lianbin 
@Version :   1.0
@Desc    :   None
'''


import urllib.request
import io,os
import sys
import json
import urllib.parse
import bs4
from bs4 import BeautifulSoup
import re
import requests

#定义输出结果的编码为utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')


class Image_downloader(object):

    def work(self,url):
        html = self.get_decoded_html(url)
        self.download_images(html)

    def get_decoded_html(self,url):
        headers = {
        'Connection':' keep-alive',
        'Pragma':' no-cache',
        'Cache-Control':' no-cache',
        'Accept':'application/json, text/plain, */*',
        'User-Agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'DNT':' 1',
        'Accept-Language':' zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'Cookie':'',
        'Accept-Encoding': ''
        }

        request = urllib.request.Request(url, headers = headers)
        response = urllib.request.urlopen(request)
        html = response.read()
        #print(html)
        html_decoded = html.decode('gbk','ignore')
        return html_decoded
    
    def download_images(self,html):
        soup = BeautifulSoup(html, 'lxml')  # lxml为解析器，可以换成其他的解析器
        table = soup.find('table', id='example') 
        td  = table.find_all('td') [0]
        result = re.search(r'(\d+)\W+([\u4e00-\u9fa5]*)\d+元', td.text, re.M|re.I)
        card_no = result.group(1)
        card_name = result.group(2)

        img_list = soup.find_all('img')  # 获取所有的img标签
        image_icon_url = "http://ka.05321888.com/ka/taocan/" + img_list[1]['src']
        image_detail_url = "http://ka.05321888.com/ka/taocan/" + img_list[2]['src']
        image_icon_name = card_name + "_图标.jpg"
        image_detail_name = card_name + "_详情.jpg"
        local_dir = "images/"

        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        with open(local_dir+image_icon_name, 'wb') as f:
            f.write(requests.get(image_icon_url).content)
        with open(local_dir+image_detail_name, 'wb') as f:
            f.write(requests.get(image_detail_url).content)

        
        

if __name__ == '__main__':
    r1 = Image_downloader()
    url = r'http://ka.05321888.com/ka/taocan/1459.html'
    r1.work(url)
    