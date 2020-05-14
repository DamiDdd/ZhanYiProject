import re

import pkuseg
import pymysql


def table_exists(conn, table_name):
    sql = "show tables;"
    conn.execute(sql)
    tables = [conn.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        return 1
    else:
        return 0


def main():
    conn = pymysql.connect(host='localhost', user='root', password='password', port=3306, db='zhanyi')
    cursor = conn.cursor()
    conn2 = pymysql.connect(host='localhost', user='root', password='password', port=3306, db='zhanyi')
    cursor2 = conn2.cursor()
    table_name = 'spider'
    if table_exists(cursor, table_name) == 1:
        cursor.execute('select * from spider')
    lexicon = ['疫中书店', '中国', '疫情']
    seg = pkuseg.pkuseg(user_dict=lexicon)
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    while True:
        row = cursor.fetchone()
        if not row:
            break
        dict = {}
        text = seg.cut(row[0] + ' ' + row[1])
        for i in text:
            match = zhPattern.search(i)
            if match:
                if dict.__contains__(i):
                    dict[i] = dict[i] + 1
                else:
                    dict[i] = 1
        dict = sorted(dict.items(), key=lambda  kv: (kv[1],kv[0]))
        cursor2.execute("update spider set fenci=(%s) where title=(%s)",(str(dict), row[0]))
        print(dict)
    conn.commit()
    cursor.close()
    conn.close()
    conn2.commit()
    cursor2.close()
    conn2.close()


if __name__ == '__main__':
    main()