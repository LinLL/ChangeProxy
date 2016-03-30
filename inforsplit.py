__author__ = 'js'

import urllib.request
import urllib.error
import os
import sys
import http.server
import http.client
import time
import re
import random
import math
import requests

home = 'http://jandan.net/ooxx'
data = None
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
enctype = 'utf-8'
proxies = []
error = None
max_error_times = 5        #最多允许失败5次，否则放弃该图片下载

def create_localhost():
    number = int((math.sqrt(5)-1)/2) * len(proxies)
    for x in range(number):
        proxies.append(None)

def get_response(req):
    error_time = 0
    while True:
        try:
            if error_time == max_error_times:
                print('失败次数达%d次......放弃操作' % max_error_times)
                return None
            error_time += 1
            response = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            if hasattr(e,'code'):
                print(e.code,e.reason)
                change_proxy()
                continue
            elif hasattr(e,'reason'):
                print(e)
                change_proxy()
                continue
        except (ConnectionResetError,http.client.BadStatusLine) as e:
            print(e)
            change_proxy()
            continue
        except TimeoutError as e:
            print(e)
            print('服务器长时间无响应，自动切换代理.....')
            change_proxy()
            continue
        return response

def get_proxy():
    global data,headers,proxies
    req = urllib.request.Request('http://www.xici.net.co',None,headers)
    response = get_response(req)
    html = response.read().decode('utf-8')
    p = re.compile(r'''<tr\sclass[^>]*>\s+
                                    <td>.+</td>\s+
                                    <td>(.*)?</td>\s+
                                    <td>(.*)?</td>\s+
                                    <td>(.*)?</td>\s+
                                    <td>(.*)?</td>\s+
                                    <td>(.*)?</td>\s+
                                    <td>(.*)?</td>\s+
                                </tr>''',re.VERBOSE)
    proxy_list = p.findall(html)
    for each_proxy in proxy_list[1:]:
        if each_proxy[4] == 'HTTP':
            proxies.append(each_proxy[0]+':'+each_proxy[1])

def change_proxy():
    proxy = random.choice(proxies)
    if proxy == None:
        proxy_support = proxy_support = urllib.request.ProxyHandler({})
    else:
        proxy_support = urllib.request.ProxyHandler({'http':proxy})
    opener = urllib.request.build_opener(proxy_support)
    opener.addheaders = [('User-Agent',headers['User-Agent'])]
    urllib.request.install_opener(opener)
    print('智能切换代理：%s' % ('本机' if proxy==None else proxy))

def get_pic(page):      #生成器，返回一个图片链接
  pass

save_path = 'D:\\图片\\马克思主义'

def download():
    count = 1
    global data,headers
    for pic_url in get_pic(1):         #get_pic(1)表示从第1页开始下载
        file_name = os.path.split(pic_url)[1]
        if not os.path.isdir(save_path):    #目录不存在就创建
            os.makedirs(save_path)
        with open('%s\\%s' % (save_path , file_name) , 'wb') as f:
            req = urllib.request.Request(pic_url,data,headers)
            response = get_response(req)
            if response == None:
                continue
            f.write(response.read())
            print('本次成功下载第%d个图片! %s' % (count , pic_url))
            count += 1




def requestproxy():
    proxies = {
      'http': '58.248.137.228:80',

    }

    headers ={"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)"}
    res = requests.get("https://www.google.com.hk/search?q=test&oq=test&aqs=chrome.0.69i59j69i60j0l4.703j0j8&sourceid=chrome&ie=UTF-8", proxies=proxies)
    print res.headers
    print res.content
    res = requests.get("https://www.google.com.hk", proxies = proxies)
    print res.text

if __name__=="__main__":

    get_proxy()
    create_localhost()
    download()
