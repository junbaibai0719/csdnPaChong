import requests
import re
from bs4 import BeautifulSoup
import threading
from queue import Queue
from threading import active_count

import usesqlit

dbname = 'test.db'

offset_url = 'https://blog.csdn.net/api/articles?type=more&category={cla}&shown_offset={offset}'

# 匹配article url的正则
rurl = '"(https://blog.csdn.net/.*?/article/.*?/[0-9]{8})"'
rurll = '"url":"(https://blog.csdn.net/.*?/article/.*?/[0-9]{8})'
# 匹配博客内容的正则
rtitle = '<title>(.+)</title>'
rcontent = '>(.+)<'
# 编译正则
com_rurl = re.compile(rurl)
com_rurll = re.compile(rurll)
com_rtitle = re.compile(rtitle)
com_rcontent = re.compile(rcontent)


# 获取博客文章的url
def get_atcurl(htmltext):
    goturl = []
    result = []
    goturl = re.findall(com_rurl, htmltext)
    goturl.extend(re.findall(com_rurll, htmltext.replace('\\', '')))
    goturl = set(goturl)
    result = list(goturl)
    return result



# 使用博客的URL爬取数据
def get_article(url):
    htmltext = requests.get(url).text
    soup = BeautifulSoup(htmltext, 'lxml')
    # 获取标题
    title = re.findall(com_rtitle, htmltext)
    # 获取标签
    lable = []
    for link in soup.find_all('a', class_='tag-link'):
        lable.append(link.text)
    lable = ''.join(lable).split('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t')
    lable = ''.join(lable)
    # 获取文章日期
    try:
        articletime = soup.find_all('span', class_='time')[0].text  # 精确时间
        ymd = re.findall('[0-9]+', articletime)
        date = articletime.split()[0].replace('年', '-').replace('月', '-').replace('日', '')  # 日期格式转换
    except IndexError:
        pass
    # 获取作者
    try:
        nickname = soup.find_all('a', class_='follow-nickName')[0].text
    except IndexError:
        pass
    # 获取文章中其他的博客链接
    otherurl = get_atcurl(htmltext)
    # 构造可以直接存入表中的数据类型
    urldata = []
    try:
        urldata.append((url, 1, title[0], nickname, ymd[0], ymd[1], ymd[2], date, lable))
    except UnboundLocalError:
        pass
    for i in otherurl:
        urldata.append((i, 0, '', '', '', '', '', '', ''))
    return urldata



class Spider(threading.Thread):
    def __init__(self, waitusequeue, dataqueue, mysql):
        super().__init__()
        self.waitusequeue = waitusequeue
        self.url = self.waitusequeue.get()
        self.dataqueue = dataqueue
        self.mysql = mysql

    def run(self):
        self.data = get_article(self.url)
        #如果返回的数据列表非空，插入待写数据队列
        if self.data != []:
            self.dataqueue.put(self.data)



if __name__ == '__main__':
    # 设置队列
    dataqueue = Queue(maxsize=100)
    waitusequeue = Queue(maxsize=200)
    mysql = usesqlit.MySql(database=dbname)
    spiders = []
    url = 'https://blog.csdn.net/nav/newarticles'
    waitusequeue.put(url)
    while True:
        #如果待爬队列为空，则从数据库中取出10条
        if  waitusequeue.empty():
            try:
                tmp = mysql.access('urldata')
                if tmp == []:
                    waitusequeue.put(url)
                for i in tmp:
                    waitusequeue.put(i[0])
            except Exception:
                pass
        #如果待爬队列不为空，且线程数量和待写数量过少则增加线程
        while waitusequeue.qsize() != 0 and active_count() <= 10 and dataqueue.qsize() < 20:
            spider = Spider(waitusequeue, dataqueue, mysql)
            spider.start()
            spiders.append(spider)
        #如果待写数据队列不为空，则写入数据
        if not dataqueue.empty():
            data = dataqueue.get()
            mysql.save(tablename='urldata', list=data)
