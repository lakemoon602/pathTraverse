# coding=utf-8
from threadpool import ThreadPool,makeRequests
import sys,re,time,os,requests
from common import is_url_live,handle_file

banner='''
 
  _____        _    _       _______                                         _ 
 |  __ \      | |  | |     |__   __|                                       | |
 | |__) |__ _ | |_ | |__      | | _ __  __ _ __   __ ___  _ __  ___   __ _ | |
 |  ___// _` || __|| '_ \     | || '__|/ _` |\ \ / // _ \| '__|/ __| / _` || |
 | |   | (_| || |_ | | | |    | || |  | (_| | \ V /|  __/| |   \__ \| (_| || |
 |_|    \__,_| \__||_| |_|    |_||_|   \__,_|  \_/  \___||_|   |___/ \__,_||_|
 author: kemoon
 github: https://github.com/lakemoon602/pathTraverse/                            
                                 
[!]start threading
[!]Dection starting...
'''
# 可自定义更改线程
max_thread=200
payloads=[]
result=[]
pool = ThreadPool(max_thread) # 设置线程池
headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }


def detect(res,payload):
    if len(res)==0:
        return False
    pattern=re.compile('<title>.+\w+.+</title>')
    data=pattern.findall(res)
    if len(data)>0 and (payload != '' and (payload in data[0]) or ("Index of" in data[0])):
        return True
    return False

def loop(schema):
    for payload in payloads:
        url=schema+'/'+payload
        #sleep(1)   #可取消此注释达到延时效果
        try:
            res=requests.get(url,headers=headers,timeout=3,allow_redirects=False)
            res.encoding = res.apparent_encoding
            if res.status_code==200:
                if detect(res.text,payload): 
                    print(url)
                    result.append(url)
                    return True
        except:
            pass
    return False

def scan(domain):
    schema="http://"+domain
    if is_url_live(schema):
        if loop(schema):
            return True

    schema="https://"+domain
    if is_url_live(schema):
        loop(schema)

if __name__=="__main__":
    print(banner)
    path= sys.argv[2] if len(sys.argv)>2 else "path_fast.txt"
    payloads=handle_file(path)
    payloads.insert(0,'')
    domains=handle_file(sys.argv[1])   
    start=time.time()
    params = [([d], None) for d in domains]
    request = makeRequests(scan, params)
    [pool.putRequest(req) for req in request]
    pool.wait()
    with open('result.txt','w') as f:
        f.writelines(result)
    print('Detection over in '+str(time.time()-start).split('.')[0]+'s')
