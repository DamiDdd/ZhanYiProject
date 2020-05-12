import xlrd
from xlutils.copy import copy


def main():
    data={
        'title': 'test',
        'content': 'test',
        'nickname': 'test',
        'date': 'test'
    }
    with open('html.txt','r',encoding='utf-8') as f:
        data['title'] = f.readline()
        data['title'] = data['title'].replace("\n","")
        data['nickname'] = f.readline()
        data['nickname'] = data['nickname'].replace("\n","")
        data['date'] = f.readline()
        data['date'] = data['date'].replace("\n","")
        data['content'] = f.read()
        data['content'] = data['content'].replace("\n"," ")
    workbook = xlrd.open_workbook('spider.xls')  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    new_worksheet.write(rows_old,0,data['title'])
    new_worksheet.write(rows_old,1,data['content'])
    new_worksheet.write(rows_old,2,data['nickname'])
    new_worksheet.write(rows_old,3,data['date'])
    new_workbook.save('spider.xls')  # 保存工作簿
    print(rows_old+1)
    print(data['title'] + ' author:' + data['nickname'] + ' date:' + data['date'] + " success")


if __name__ == '__main__':
    main()
