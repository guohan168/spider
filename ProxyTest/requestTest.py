import requests

# 测试requests头部添加header请求
def testAddHeaders():
    params={"appname":"Car","TuserId":24126018}
    url="https://i.autohome.com.cn/ajax/home/OtherHomeAppsData"
    headers=dict()
    headers.__setitem__("Host","i.autohome.com.cn")
    headers.__setitem__("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:64.0) Gecko/20100101 Firefox/64.0")
    headers.__setitem__("Accept","*/*")
    headers.__setitem__("Accept-Language","zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2")
    headers.__setitem__("Accept-Encoding","gzip, deflate, br")
    headers.__setitem__("Referer","https://i.autohome.com.cn/1521649")
    headers.__setitem__("X-Requested-With","XMLHttpRequest")
    headers.__setitem__("Connection","keep-alive")
    headers.__setitem__("Pragma","no-cache")
    headers.__setitem__("Cache-Control","no-cache")
    r=requests.get(url=url,params=params,headers=headers)
    print(r.text)
    j=r.json()
    print(type(j))


testAddHeaders()


