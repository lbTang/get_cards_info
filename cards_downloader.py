# -*- encoding: utf-8 -*-
'''
@File    :   cards_downloader.py
@Time    :   2021/01/25 20:26:35
@Author  :   Tang Lianbin 
@Version :   1.0
@Desc    :   None
'''

import io,os,sys
import json
import bs4
from bs4 import BeautifulSoup
import xlwt
import sqlite3
import re
import requests
import time

#定义输出结果的编码为utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

class cards_downloader(object):

    def get_decoded_html(self,url):
        html = requests.get(url).content
        return html.decode('gbk','ignore')
    
    def get_cards_info(self,html):
        soup = BeautifulSoup(html,"html.parser",from_encoding="gbk")
        tbody = soup.find_all('tbody')[0]


        cards_info = []
        for tr in tbody.children:
            if isinstance(tr,bs4.element.Tag):
                td = tr.find('td')
                text = td.text
                code = re.findall(r'\d+',text)[0]
                if (code!='0038'):
                    result = re.match(r'(\d+)?.*?([\u4e00-\u9fa5]+)(\d+元*)包*(.*)', text, re.M|re.I)
                    card_no = result.group(1) #1.流量卡编号
                    card_name = result.group(2) #2.卡名
                    full_name = text #3.完整卡名
                    monthly_cost = result.group(3) #4.月租
                    if monthly_cost[-1] in '0123456789':
                        monthly_cost+='元'
                    plan_detail = result.group(4) #5.套餐流量
                    addition = '' # addition =  #6.附加说明
                    for i in tr.find_all('i'):
                        if(i.text != ""):
                            addition=addition+'|'+i.text
                    detail_url = 'http://ka.05321888.com/ka/taocan/'+ card_no + '.html' #7.详情链接              
                cards_info.append({'card_no':card_no,'card_name':card_name,'plan_detail':plan_detail,'addition':addition,'monthly_cost':monthly_cost,'full_name':full_name,'detail_url':detail_url})
        return cards_info

    def connect_sqlite(self,cards_data):
        con = sqlite3.connect("cards_data.db")
        cur = con.cursor()
        # no:编号； card_name:卡名； addition:附加优惠信息； detail_url:套餐链接； ispublish:是否发布； state:生效状态
        cur.execute("CREATE TABLE IF NOT EXISTS cards(no, card_name, addition, monthly_cost, detail_url, ispublish, state)")
        fetch_cardNos = cur.execute("SELECT no FROM cards").fetchall()
        card_no_list = [item[0] for item in fetch_cardNos]
        for card in cards_data:
            if card['code'] not in card_no_list:
                cur.execute("""INSERT INTO cards VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (card["code"],card["card_name"],card["addition"],card["monthly_cost"],card["detail_url"],0,1)
                )
        con.commit()
        res = cur.execute("SELECT * FROM cards")
        #print(res.fetchall())
        self.export_excel_from_db(res.fetchall())

    def work(self):
        url = r'http://ka.05321888.com/ka/taocan/index.html'
        html = self.get_decoded_html(url)
        # print(html)
        cards_info = self.get_cards_info(html)
        return cards_info

                

if __name__ == '__main__':
    r1 = cards_downloader()
    card_info = r1.work()