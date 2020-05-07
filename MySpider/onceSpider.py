import random
import re
import time
from urllib.parse import urlencode
import pymysql
import requests
import json
from bs4 import BeautifulSoup


UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
headers1 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Host": "weixin.sogou.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": UserAgent,
}
keyword = '疫'
max_count = 5


def get_response(url, count=1):
    print('Crawling ', url)
    print('Trying Count', count)
    if count >= max_count:
        print('Tried too many Counts')
        return None
    try:
        response = requests.get(url, allow_redirects=False, headers=headers1)
        if response.status_code == 200:
            return response
        if response.status_code == 302:
            print('302')
    except ConnectionError as e:
        print('Error Occure', e.args)
        count += 1
        return get_response(url, count)


# 获得urls
def get_index(page, keyword):
    timestamp = int(round(time.time() * 1000))
    data = {
        'query': keyword,
        '_sug_type_': None,
        'sut': '0',
        'lkt': '0,0,0',
        's_from': 'input',
        '_sug_': 'n',
        'type': '2',
        'sst0': timestamp,
        'page': page,
        'ie': 'utf8',
        'w': '01015002',
        'dr': '1'
    }
    url = 'https://weixin.sogou.com/weixin?' + urlencode(data)
    response = get_response(url)
    return response


def get_k_h(url):
    b = int(random.random() * 100) + 1
    a = url.find("url=")
    url = "http://weixin.sogou.com" + url + "&k=" + str(b) + "&h=" + url[a + 4 + 21 + b: a + 4 + 21 + b + 1]
    return url


def get_uigs_para(response):
    uigs_para = re.findall('var uigs_para = (.*?);', response.text, re.S)[0]
    if 'passportUserId ? "1" : "0"' in uigs_para:
        uigs_para = uigs_para.replace('passportUserId ? "1" : "0"', '0')
    uigs_para = json.loads(uigs_para)
    exp_id = re.findall('uigs_para.exp_id = "(.*?)";', response.text, re.S)[0]
    uigs_para['right'] = 'right0_0'
    uigs_para['exp_id'] = exp_id[:-1]
    return uigs_para


def get_cookie(response1, uigs_para):
    SetCookie = response1.headers['Set-Cookie']
    cookie_params = {
        "ABTEST": re.findall('ABTEST=(.*?);', SetCookie, re.S)[0],
        "SNUID": re.findall('SNUID=(.*?);', SetCookie, re.S)[0],
        "IPLOC": re.findall('IPLOC=(.*?);', SetCookie, re.S)[0],
        "SUID": re.findall('SUID=(.*?);', SetCookie, re.S)[0]
    }

    url = "https://www.sogou.com/sug/css/m3.min.v.7.css"
    headers = {
        "Accept": "text/css,*/*;q=0.1",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "SNUID={}; IPLOC={}".format(cookie_params['SNUID'], cookie_params['IPLOC']),
        "Host": "www.sogou.com",
        "Referer": "https://weixin.sogou.com/",
        "User-Agent": UserAgent
    }
    response2 = requests.get(url, headers=headers)
    SetCookie = response2.headers['Set-Cookie']
    cookie_params['SUID'] = re.findall('SUID=(.*?);', SetCookie, re.S)[0]

    url = "https://weixin.sogou.com/websearch/wexinurlenc_sogou_profile.jsp"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "ABTEST={}; SNUID={}; IPLOC={}; SUID={}".format(cookie_params['ABTEST'], cookie_params['SNUID'],
                                                                  cookie_params['IPLOC'],
                                                                  cookie_params['SUID']),
        "Host": "weixin.sogou.com",
        "Referer": response1.url,
        "User-Agent": UserAgent
    }
    response3 = requests.get(url, headers=headers)
    SetCookie = response3.headers['Set-Cookie']
    cookie_params['JSESSIONID'] = re.findall('JSESSIONID=(.*?);', SetCookie, re.S)[0]

    url = "https://pb.sogou.com/pv.gif"
    headers = {
        "Accept": "image/webp,*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "SNUID={}; IPLOC={}; SUID={}".format(cookie_params['SNUID'], cookie_params['IPLOC'],
                                                       cookie_params['SUID']),
        "Host": "pb.sogou.com",
        "Referer": "https://weixin.sogou.com/",
        "User-Agent": UserAgent
    }
    response4 = requests.get(url, headers=headers, params=uigs_para)
    SetCookie = response4.headers['Set-Cookie']
    cookie_params['SUV'] = re.findall('SUV=(.*?);', SetCookie, re.S)[0]

    return cookie_params


def parse_index(html):
    compile = re.compile('<div.*?class="txt-box">.*?<h3>.*?<a.*?target="_blank".*?href="(.*?)".*?id=".*?">.*?</a>', re.S)
    # print(html)
    results = re.findall(compile, html)
    for result in results:
        result = result.replace('amp;', '')
        result = get_k_h(result)
        yield {
            'url': result
        }


def get_detail(params, url):
    headers3 = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "ABTEST={}; SNUID={}; IPLOC={}; SUID={}; JSESSIONID={}; SUV={}".format(params['ABTEST'],
                                                                                         params['SNUID'],
                                                                                         params['IPLOC'],
                                                                                         params['SUID'],
                                                                                         params['JSESSIONID'],
                                                                                         params['SUV']),
        "Host": "weixin.sogou.com",
        "Referer": 'https://weixin.sogou.com/',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": UserAgent
    }
    response3 = requests.get(url, headers=headers3)
    fragments = re.findall("url \+= '(.*?)'", response3.text, re.S)
    itemurl = ''
    for i in fragments:
        itemurl += i

    # 文章url拿正文
    headers4 = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "max-age=0",
        "user-agent": UserAgent
    }
    try:
        response4 = requests.get(itemurl, headers=headers4)
        # response = requests.get(url, headers=headers4)
        if response4.status_code == 200:
            return response4.text
        return None
    except ConnectionError:
        return None


def parse_detail(response):
    soup = BeautifulSoup(response, 'lxml')
    try:
        # 获得具体的信息
        title = soup.select('#activity-name')[0].get_text().strip()
        nickname = soup.select('#js_profile_qrcode > div > strong')[0].get_text().strip()
        content = soup.select('#js_content')[0].get_text().strip()
        wechat = soup.select('#js_profile_qrcode > div > p:nth-child(3) > span')[0].get_text().strip()
        date = re.findall('var.*?publish_time.*?= "(.*?)".*?;', response)[0]
        print(title,nickname,content,wechat,date)
        return {
            'title': title,
            'content': content,
            'nickname': nickname,
            'wechat': wechat,
            'date': date
        }
    except:
        return {
            'title': None,
            'content': None,
            'nickname': None,
            'wechat': None,
            'date': None
        }


def insert_into_mysql(data):
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

    conn = pymysql.connect(host='localhost', user='root', password='password', port=3306, db='zhanyi')
    cursor = conn.cursor()
    table_name = 'spider'
    if table_exists(cursor, table_name) != 1:
        cursor.execute(
            'create table spider(title varchar(100),content text ,nickname varchar(50) ,wechat varchar(30),date varchar(30)) ENGINE=InnoDB DEFAULT character set utf8mb4 collate utf8mb4_general_ci;')
    title = data['title']
    content = data['content']
    nickname = data['nickname']
    wechat = data['wechat']
    date = data['date']
    try:
        cursor.execute("insert into spider (title,content,nickname,wechat,date) values (%s,%s,%s,%s,%s)",
                       (title, content, nickname, wechat, date))
    except:
        print(1)
        pass
    conn.commit()
    cursor.close()
    conn.close()


def save_to_csv(data):
    title = data['title']
    content = data['content']
    nickname = data['nickname']
    wechat = data['wechat']
    date = data['date']
    try:
        with open('spider.csv', 'a', newline='', encoding='utf-8-sig')as f:
            f.write(
                title + ',' + content + ',' + nickname + ',' + wechat + ',' + date)
            f.write('\n')
            f.close()
    except:
        pass


def helper_visit(params, response1):
    headers2 = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": "ABTEST={}; IPLOC={}; SUID={}; SUV={}; SNUID={}; JSESSIONID={};".format(params['ABTEST'],
                                                                                          params['IPLOC'],
                                                                                          params['SUID'], params['SUV'],
                                                                                          params['SNUID'],
                                                                                          params['JSESSIONID']),
        "Host": "weixin.sogou.com",
        "Referer": response1.url,
        "User-Agent": UserAgent,
        "X-Requested-With": "XMLHttpRequest"
    }
    return headers2


def main():
    for i in range(1, 2):
    # for i in range(1, 101):
        print('crawl page number:', i)
        time.sleep(10 + random.random())
        response1 = get_index(i, keyword)
        html = response1.text
        uigs_para = get_uigs_para(response1)
        params = get_cookie(response1, uigs_para)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                # response2 = requests.get(approve_url, headers=headers2)
                article_url = article_url['url']
                article_html = get_detail(params, article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    insert_into_mysql(article_data)
                    save_to_csv(article_data)


if __name__ == '__main__':
    main()
