#coding=utf-8
from bs4 import BeautifulSoup
import urllib, urllib2, time, cookielib, json, logging, traceback
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
        counter[t] += 1
        if activity.next_sibling.next_sibling == None:
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
                continue

        activity = activity.next_sibling.next_sibling
    f_write(name, business, counter)
   
def f_write(name, business, counter):
    f_name = 'user_data.txt'
    data = [0, 0, 0, 0, 0] 
    data[0] = str(int(np.sum(counter[6:10])))
    data[1] = str(int(np.sum(counter[11:12])))
    data[2] = str(int(np.sum(counter[13:17])))
    data[3] = str(int(np.sum(counter[18:22])))
    data[4] = str(int(np.sum(counter) - np.sum(counter[6:22])))
    with open('user_data.txt', 'a') as f:
        f.write(name + "\t" + business + "\t" + "\t".join(data) + "\t" + str(np.sum(counter)) + "\n")
    logging.info("%s download."%name) 



