#coding=utf-8
import urllib
import urllib2
import cookielib
import json
import time, logging
from PIL import Image

#第一次登陆，用验证码登陆
def login():
    #cookie init
    cookies = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    urllib2.install_opener(opener)

    c =  urllib2.urlopen('http://www.zhihu.com')

    #验证码处理
    d =  urllib2.urlopen('https://www.zhihu.com/captcha.gif?r=%s&type=login'%str(time.time() * 1000))
    with open('captcha.gif', 'wb') as f:
        f.write(d.read())
    print '输入验证码'
    Image.open('captcha.gif').show()
    captcha = raw_input()

    #login
    form =  {}
    for cookie in cookies:
        if cookie.name == '_xsrf' :
            form['_xsrf'] = cookie.value
    form['password'] = ''
    form['phone_num'] = ''
    form['remember_me'] = False
    form['captcha'] = captcha

    post_data=urllib.urlencode(form)
    headers ={"User-agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
    req=urllib2.Request('https://www.zhihu.com/login/phone_num',post_data,headers)
    content=json.load(opener.open(req))

    if content['r'] == 0 :
        print content['msg']
        cookies.save('cookie.txt', ignore_discard=True, ignore_expires=True)
        logging.info('登陆成功')
    else: 
        if data in content: 
            print content['msg']
            logging.info('登陆失败 %s' %content['msg'])
            exit()

#保存过cookie，可以直接load
def load_cookies():
    try:
        # 创建MozillaCookieJar实例对象
        cookie = cookielib.MozillaCookieJar()
        # 从文件中读取cookie内容到变量
        cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
        # 利用urllib2的build_opener方法创建一个opener
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        urllib2.install_opener(opener)
        logging.info('载入cookies成功')
    except:
        login()






