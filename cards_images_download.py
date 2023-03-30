# -*- encoding: utf-8 -*-
'''
@File    :   card_downloader.py
@Time    :   2021/01/25 20:26:35
@Author  :   Tang Lianbin 
@Version :   1.0
@Desc    :   None
'''


import io,os
import sys
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
        response = requests.get(url)
        html = response.content
        code = response.status_code
        html_decoded = html.decode('gbk','ignore')
        return [html_decoded,code]
    
    def download_images(self,url,local_dir = "cards/"):
        html,code = self.get_decoded_html(url)
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
        
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        with open(local_dir+image_icon_name, 'wb') as f:
            f.write(requests.get(image_icon_url).content)
        with open(local_dir+image_detail_name, 'wb') as f:
            f.write(requests.get(image_detail_url).content)
    
    def download_html_file(self,url,local_dir="cards/"):
        html,code = self.get_decoded_html(url)
        if code == 200:
            soup = BeautifulSoup(html, 'lxml')  # lxml为解析器，可以换成其他的解析器
            tables = soup.find_all('table')
            if tables:
                td = tables[0].find_all('td')[0]
                result = re.search(r'(\d+)\W+([\u4e00-\u9fa5]*)\d+元', td.text, re.M|re.I)
                card_no = result.group(1)
                card_name = result.group(2)

                file_name = card_no + '_' + card_name + '.html'
                local_dir = local_dir + card_no + '_' + card_name + "/"
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)
                with open(local_dir+file_name, "wb") as f:
                    #   写文件用bytes而不是str，所以要转码
                    f.write(bytes(html, encoding = "gbk"))

                decode_html,code = self.get_decoded_html(url)
                
                soup = BeautifulSoup(decode_html, 'lxml')  # lxml为解析器，可以换成其他的解析器
                

                img_list = soup.find_all('img')  # 获取所有的img标签
                for img in img_list:
                    filename = img['src']
                    img_url = "http://ka.05321888.com/ka/taocan/xiangguan/"+filename
                    with open(local_dir+filename, 'wb') as f:  
                        r = requests.get(img_url) 
                        f.write(r.content)
            else:
                file_name = url.split('/')[-1]
                local_dir = local_dir + file_name.split('.')[0] + "/"
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)
                with open(local_dir+file_name, "wb") as f:
                    #   写文件用bytes而不是str，所以要转码
                    f.write(bytes(html, encoding = "gbk"))



        

if __name__ == '__main__':
    r1 = Image_downloader()
    url = r'http://ka.05321888.com/ka/taocan/xiangguan/1454.html'
    # r1.work(url)
    r1.download_html_file(url)
    