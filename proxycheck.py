#encoding=gbk
import requests
import time
import urllib
import threading
#import GetProxy
import lxml

inFile = open('proxy.txt', 'r')
outFile = open('available.txt', 'w')

lock = threading.Lock()

def test():
    while True:
        lock.acquire()
        line = inFile.readline().strip()
        lock.release()
        if len(line) == 0: break
        protocol, proxy = line.split('=')
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': ''}
        proxies = {"http":"http://"+proxy}

        try:
            res = requests.get("https://www.google.com.hk/search?q=test&oq=test&aqs=chrome.0.69i59j69i60j0l4.703j0j8&sourceid=chrome&ie=UTF-8", proxies=proxies,timeout=5)
            #res = requests.get("https://www.facebook.com/", proxies=proxies,timeout=1)
            #res = requests.get("http://ip.cn",proxies=proxies)
            print proxies["http"]+"!!!!!"+str(res.status_code)
            if  res.status_code==200:
                lock.acquire()
                print 'add proxy', proxy["http"]
                outFile.write(proxy + '\n')
                lock.release()
                print '.',
        except Exception, e:
            print e

all_thread = []
for i in range(50):
    t = threading.Thread(target=test)
    all_thread.append(t)
    t.start()

for t in all_thread:
    t.join()
inFile.close()
outFile.close()
