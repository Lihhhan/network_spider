#coding=utf-8
import urllib
import urllib2
import cookielib
import json
import time
from PIL import Image

def login():
    #cookie init
    cookies = cookielib.CookieJar()
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
    form['phone_num'] = '18742517035'
    form['remember_me'] = False
    form['captcha'] = captcha

    post_data=urllib.urlencode(form)
    headers ={"User-agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
    req=urllib2.Request('https://www.zhihu.com/login/phone_num',post_data,headers)
    content=json.load(opener.open(req))

    print content
    if content['r'] == 0 :
        print content['msg']
    else: 
        if data in content: 
            print content['msg']    
            exit()

