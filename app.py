#coding=utf-8
import login, spider
import sys, logging
import conf, traceback

reload(sys)
sys.setdefaultencoding( "utf-8" )

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='myapp.log',
    filemode='a')

login.load_cookies()
#spider.run_with_time("test","niuzijian")
for (f_name, job) in conf.jobs.items():
    for person in job:
        try:
            logging.info('%s start..'%person)
            spider.run_with_time(f_name, person)
        except:
            logging.info('%s download error, skip...\n%s'%(person, traceback.format_exc()))
            continue

logging.info('task end.')



