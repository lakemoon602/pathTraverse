import requests,re

def is_url_live(url):
    headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
    try:
        requests.get(url,headers,timeout=3)
        return True
    except:
        return False

def handle_file(filename):
    data=[]
    with open(filename,'r') as f:
        for line in f:
            data.append(line[:-1])
    return list(set(data))

