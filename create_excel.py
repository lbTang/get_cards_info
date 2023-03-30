# -*- encoding: utf-8 -*-
'''
@File    :   create_excel.py
@Time    :   2023/03/29 14:40:41
@Author  :   Tang Lianbin 
@Version :   1.0
@Desc    :   None
'''

# put the import lib here
import io
import sys
import xlsxwriter



class Robot(object):

    def work(self):
        workbook = xlsxwriter.Workbook('hello.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'Hello world')
        workbook.close()


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
    r1 = Robot()
    r1.work()