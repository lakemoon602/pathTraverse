# coding=utf-8
import requests
import sys
import re
import time
import threading
import os
import sys

banner='''
 
  _____        _    _       _______                                         _ 
 |  __ \      | |  | |     |__   __|                                       | |
 | |__) |__ _ | |_ | |__      | | _ __  __ _ __   __ ___  _ __  ___   __ _ | |
 |  ___// _` || __|| '_ \     | || '__|/ _` |\ \ / // _ \| '__|/ __| / _` || |
 | |   | (_| || |_ | | | |    | || |  | (_| | \ V /|  __/| |   \__ \| (_| || |
 |_|    \__,_| \__||_| |_|    |_||_|   \__,_|  \_/  \___||_|   |___/ \__,_||_|
                                                                             
                                 
                                 
[!]start threading
[!]Dection starting...
'''

max_thread=200
https="https://"
http="http://"
domains=[]
dict=[]
res=[]
headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
#获取域名
def getDomain(file):
    with open(file,'r',encoding='UTF-8') as f:
    	for line in f:
    		domains.append(line[:-1])
    	f.close()
            
#获取字典
def getDict(filename):
    with open(filename,'r',encoding='UTF-8') as f:
        for line in f:
            dict.append(line[:-1])
    f.close()

#清洗数据
def clear(domain):
    flag=0
    for mem in res:
        if mem.find(domain)>0:
            flag+=1
            if flag>=10:
                return False
    return True

#目录遍历poc
def target(res,dic):

    if len(res)==0:
        return False
    pattern=re.compile('<title>.+\w+.+</title>')
    data=pattern.findall(res)
    if len(data)>0 and dic in data[0]:
        return True
    return False

#扫描模块
def scan(domain):
    for dictionary in dict:
        http_req_url=http+domain+'/'+dictionary
        https_req_url=https+domain+'/'+dictionary

        try:
            resHttp=requests.get(http_req_url,headers=headers,timeout=3,allow_redirects=False)
            resHttp.encoding = resHttp.apparent_encoding
            if int(resHttp.status_code)==200:
                if clear(domain) and target(resHttp.text,dictionary): 
                    print(http_req_url)
                    res.append(http_req_url+'\n')
            time.sleep(1)
        except:
            pass
        try:
            resHttps=requests.get(https_req_url,headers=headers,timeout=3,allow_redirects=False)
            resHttps.encoding=resHttps.apparent_encoding
            if int(resHttps.status_code)==200:
                if clear(domain) and target(resHttps.text,dictionary): 
                    print(https_req_url)
                    res.append(https_req_url+'\n')
        except:
            pass

if __name__=="__main__":

    print(banner)
    # 获取字典
    getDict("path.txt")
    #获取域名
    getDomain(sys.argv[1])
    thread=[]
    #多线程调用
    #daemon参数，主线程随子线程结束还是子线程随主线程结束,默认为False
    start=time.time()
    for domain in domains:
        t=threading.Thread(target=scan,args=(domain,),daemon=True)
        thread.append(t)
    
    #维持线程队列
    for t in thread:
        t.start()
        while True:
            if len(threading.enumerate())<=max_thread:
                time.sleep(1)
                break
            
    while True:
        if len(threading.enumerate())<2:
            break
        time.sleep(10)
        
    print('Detection over in '+str(time.time()-start).split('.')[0]+'s')

    #保存检测结果
    with open('result.txt','w') as f:
        for line in res:
            f.write(line+'\n')
        f.close()

