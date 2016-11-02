#coding=utf-8
import login, spider
import sys, logging
import conf, traceback, Queue

reload(sys)
sys.setdefaultencoding( "utf-8" )

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='myapp2.log',
    filemode='a')

login.load_cookies()

persons = Queue.Queue(maxsize = -1)
person_list = {}

#spider.followers("niuzijian")
#spider.run_with_time("test","niuzijian")
#热启动
for (f_name, job) in conf.jobs.items():
    for p in job:
       persons.put(p)

logging.info('task start..')
while not persons.empty():
    person = persons.get()
    try:
        logging.info(person + ' followers start..')
        follows = spider.followers(person)
        with open("followers.txt", 'a') as f:
            f.write(person  + '\t' + '\t'.join(follows) + '\n')
        f.close()
        for follow in follows:
            #没处理过的人，加入队列尾
            if follow not in person_list:
               persons.put(follow)


        #开始爬这个人的动态,先把他添加到处理过的人list里面
        if person not in person_list:
            person_list[person] = '1'
            logging.info(person + 'person start..')
            spider.run_with_counter('user_data', person)
    except:
        logging.info('%s error skip ..\n%s' %(person, traceback.format_exc()))

logging.info('task end.')



