# -*- encoding: utf-8 -*-
'''
@File    :   card_downloader.py
@Time    :   2021/01/25 20:26:35
@Author  :   Tang Lianbin 
@Version :   1.0
@Desc    :   None
'''


import io
import sys
import bs4
from bs4 import BeautifulSoup
import xlwt
import sqlite3
import re
import requests
from cards_images_download import Image_downloader
import json

#定义输出结果的编码为utf-8
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')


class Robot(object):

    def get_decoded_html(self,url):
        response = requests.get(url)
        html = response.content
        html_decoded = html.decode('utf8','ignore')
        return html_decoded
    
    def get_cards_data(self,html):
        soup = BeautifulSoup(html,"html.parser",from_encoding="gbk")
        tbody = soup.find_all('tbody')[0]

        result = []
        for tr in tbody.children:
            if isinstance(tr,bs4.element.Tag):
                # 接口信息：
                # 1.card_no:编号； 
                # 2.card_name:卡名； 
                # 3.addition:附加优惠信息； 
                # 4.monthly_cost:月租;
                # 5.detail_image_url:详细图片信息； 
                # 6.detail_info_url:详细说明信息;             

                #（1）card_no编号
                page = tr['onclick'].split('\'')[1]
                card_no = page.split('.')[0]
                
                #（2）card_name卡名
                td = tr.find('td')
                card_name = td.text
                #（3）addition附加优惠信息
                addition = ''
                #（4）monthly_cost月租
                if (card_no!='0038'):
                    monthly_cost = re.search(r'(\d+元*)包', card_name, re.M|re.I).group(1)
                    if monthly_cost[-1] in '0123456789':
                        monthly_cost+='元'
                else:
                    monthly_cost = ''

                for i in tr.find_all('i'):
                    if(i.text != ""):
                        addition=addition+' '+i.text
                #（5）detail_image_url:详细图片信息
                detail_image_url = "http://ka.05321888.com/ka/taocan/"+ card_no + ".html"
                # （6）detail_info_url:详细说明信息
                detail_info_url = "http://ka.05321888.com/ka/taocan/xiangguan/"+ card_no + ".html"

                result.append({'card_no':card_no,'card_name':card_name,'addition':addition,'monthly_cost':monthly_cost,'detail_image_url':detail_image_url,'detail_info_url':detail_info_url})
        return result
    

    def export_excel(self,cards_data):
        wb = xlwt.Workbook()
        ws = wb.add_sheet('sheet1')
        # 写入第一行内容  ws.write(a, b, c)  a：行，b：列，c：内容
        titleList = ['编号', '卡名', '附加', '月租','详细图片信息','发布状态']
        for i in range(0, len(titleList)):
            ws.write(0, i, titleList[i])

        # 所需获取数据对应key
        jsonKeyLIst = ['card_no','card_name','addition','monthly_cost','detail_image_url','detail_info_url']

        for i in range(0, len(cards_data)):
            for j in range(0, len(jsonKeyLIst)):
                # 文件中已写入一行title，所以这里写入内容时行号为i+1而非i
                # 列号为j
                ws.write(i + 1, j, cards_data[i][jsonKeyLIst[j]])

        # 保存文件
        wb.save('./流量套餐列表.csv')
        wb.save('./流量套餐列表.xls')


    def write_into_db(self,cards_data):
        con = sqlite3.connect("cards_data.db")
        cur = con.cursor()
        # 1.card_no:编号； 
        # 2.card_name:卡名； 
        # 3.addition:附加优惠信息； 
        # 4.monthly_cost:月租;
        # 5.detail_image_url:详细图片信息； 
        # 6.detail_info_url:详细说明信息; 
        # 7.ispublish:是否发布； 
        # 8.state:生效状态
        cur.execute("CREATE TABLE IF NOT EXISTS cards(card_no, card_name, addition, monthly_cost, detail_image_url, detail_info_url, ispublish, state)")
        fetch_cardNos = cur.execute("SELECT card_no FROM cards").fetchall()
        card_no_list = [item[0] for item in fetch_cardNos]
        for card in cards_data:
            if card['card_no'] not in card_no_list:
                cur.execute("""INSERT INTO cards VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (card["card_no"],card["card_name"],card["addition"],card["monthly_cost"],card["detail_image_url"],card["detail_info_url"],0,1)
                )
        con.commit()
        res = cur.execute("SELECT * FROM cards")
        #print(res.fetchall())
        #self.export_excel_from_db(res.fetchall())

        
    
    def download_images(self,cards_data):
        img_downloader = Image_downloader()
        for card in cards_data:
            img_downloader.download_images(card['detail_image_url'])
            img_downloader.download_html_file(card['detail_info_url'])
        
    def work(self):
        # url = r'http://tcdq.05321888.com/page/taocan/index.html'
        # html = self.get_decoded_html(url)
        url = r"http://43.139.67.76:92/tcdq_1?cz=&lx=undefined&limit=999"
        response = requests.get(url)
        r1 = response.content.decode('gbk','ignore')
        print(r1)
        j1  = json.loads(r1)
        print(j1['count'])
        
        cards_list = j1['data']
        for card in cards_list:
            # 1.card_id:编号； 
            card_id = card['id']
            # 2.card_name:卡名； 
            cardInfo = card['bt'].split(' ')[-1].split('+')
            result = re.match(r'^(.*卡)(\d+元)包*(\d+[G|M].*)?$',cardInfo[0])
            card_name = result.group(1) 
            # 3.addition:附加信息； 
            addition = ""
            if (len(cardInfo)>2):
                for item in cardInfo[2:]:
                    addition += item+" "
            # 4.monthly_cost:月租;
            monthly_cost = int(re.search(r'\d+',result.group(2)).group(0))
            # 5.generic_traffic:通用流量
            generic_traffic = int(re.search(r'\d+',result.group(3)).group(0))
            # 6.detail_info_url:详细说明信息; 
            detail_info_url = "http://tcdq.05321888.com/page/taocan/xq.html?id="+str(card_id)

            # 7.icon_image_url:图标链接； 
            # 7.detail_image_url:详细介绍链接； 
            # 8.ispublish:是否发布,0未发布，1已发布； 
            ispublish = 0
            # 9.state:生效状态，0下架，1在架；
            state = 1
        # cards_info = self.get_cards_data(r1)
        # print(cards_info)
        # self.write_into_db(cards_info)
        # self.download_images(cards_info)


if __name__ == '__main__':
    r1 = Robot()
    r1.work()
