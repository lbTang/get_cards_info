# -*- encoding: utf-8 -*-
'''
@File    :   get_request.py
@Time    :   2023/03/30 11:24:37
@Author  :   Tang Lianbin 
@Version :   1.0
@Desc    :   None
'''

# put the import lib here
import io
import sys
import requests

class Robot(object):

    def work(self):
        url = "http://tcdq.05321888.com/page/taocan/xgzl.html"
        headers = {
            'Host': 'tcdq.05321888.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:111.0) Gecko/20100101 Firefox/111.0',
            'Connection': 'keep-alive',
            'Pragma':'no-cache',
            'Cache-Control':'no-cache',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'DNT':'1',
            'Accept-Language':'en-US,en;q=0.5',
            'Cookie':'',
            'Accept-Encoding': 'gzip, deflate',
        }

        response = requests.get(url,headers=headers)
        html = response
        print(html)



if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
    r1 = Robot()
    r1.work()