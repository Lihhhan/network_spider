#coding=utf-8
from bs4 import BeautifulSoup
import urllib, urllib2, time, cookielib, json, logging, traceback, datetime
import numpy as np

def run(name, num=200):
    url = 'http://www.zhihu.com/people/' + name  
    req = urllib2.Request(url)
    c = urllib2.urlopen(req)

    cookies = cookielib.MozillaCookieJar()
    cookies.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    for cookie in cookies:
        if cookie.name == '_xsrf':
            xsrf = cookie.value

    #时间部分，只关注小时
    tformat = '%H'
    ymdformat = '%y, %m, %d'
    counter = np.zeros(24)    
    
    #数据处理
    content = BeautifulSoup(c.read())
    try:
        business = content.find('span', attrs={'class' :"business item"})['title']
    except:
        business = '未知'

    activitys = content.find(id = "zh-profile-activity-page-list")
    activity = activitys.div
    while True:
        t = int(time.strftime(tformat, time.localtime(int(activity['data-time']))))
        ymd = time.strftime(ymdformat, time.localtime(int(activity['data-time'])))
        y, m, d = ymd.split(',')
        print y,m,d
        #只计数工作日
        if int(datetime.datetime(int(y), int(m), int(d)).weekday()) < 5:
            counter[t] += 1
        if activity.next_sibling == None or activity.next_sibling.next_sibling == None:
            if np.sum(counter) >= num:
                break
            else:
                url_2 = 'http://www.zhihu.com/people/' + name + '/activities'
                headers ={"User-agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1",  
                        "X-Xsrftoken":xsrf,
                        "Referer":url, 
                        "Origin":"http://www.zhihu.com",
                        "X-Requested-With":"XMLHttpRequest",
                        "Accept":"*/*",
                        "Accept-Language":"zh-CN,zh;q=0.8",
                        "Connection":"keep-alive",
                        "Content-Length":"16",
                        "Host":"www.zhihu.com"}
                req = urllib2.Request(url_2, urllib.urlencode({'start' : int(activity['data-time'])}), headers)
                res = json.load(urllib2.urlopen(req))

                activity = BeautifulSoup(res['msg'][1]).div
                if activity == None or activity.next_sibling == None:
                    break
                continue

        activity = activity.next_sibling.next_sibling
    f_write(name, business, counter)
   
def f_write(name, business, counter):
    f_name = 'user_data.txt'
    with open('user_data.txt', 'a') as f:
        f.write(name + "\t" + business + "\t")
        for i in counter:
            f.write(str(i) + "\t")
        f.write(str(np.sum(counter)) + "\n")
    logging.info("%s download."%name) 



