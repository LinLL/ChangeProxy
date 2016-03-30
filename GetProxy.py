from bs4 import BeautifulSoup
import urllib2,sys,threading,requests,base64,re
from multiprocessing.dummy import Pool

lock = threading.Lock()
pages = range(1,20)
pa = re.compile(r'(rot13\(")([\w=]+)')
with open("proxy.txt",'w') as of:
    of.write("")

def proxyPage(page):
    headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    try:
        req = requests.get('https://www.cool-proxy.net/proxies/http_proxy_list/page:{page}/sort:score/direction:desc'.format(page=page), headers=headers)
    except requests.exceptions.ConnectionError,e:
        pass
    html_doc = req.text
    soup = BeautifulSoup(html_doc,'lxml')
    trs = soup.find_all(class_="time")
    trs = [item.find_parent() for item in trs]
    for tr in trs:
        tds = tr.find_all('td')
        ip = pa.search(tds[0].string).group(2)
        ip = base64.b64decode(ip.decode("rot13"))
        port = tds[1].text.strip()
        protocol = "HTTP"
        if protocol == 'HTTP' or protocol == 'HTTPS':
            lock.acquire()
            with open("proxy.txt","a+") as of:
                of.write('%s=%s:%s\n' % (protocol, ip, port) )
            lock.release()
            #print '%s=%s:%s' % (protocol, ip, port)

pool = Pool(16)
def run(pages):
    try:
        pool.map(proxyPage,pages)
    except urllib2.HTTPError,e:
        run(e.geturl().split('/')[-1])

if __name__=="__main__":
    run(pages)
