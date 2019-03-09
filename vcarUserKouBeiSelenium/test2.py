# -*- coding:utf-8 -*-
import requests
from lxml import html
import re
from fontTools.ttLib import TTFont

#抓取autohome评论
class AutoSpider:
    #页面初始化
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
        }
    # 获取评论
    def getNote(self):
        url = "https://club.autohome.com.cn/bbs/thread-c-2778-69436529-1.html"
        host = {'host':'club.autohome.com.cn',
                'cookie':'Hm_lvt_9924a05a5a75caf05dbbfb51af638b07=1513262213; UM_distinctid=1605574e7e020-0de43f6989305c-5a442916-100200-1605574e7e1262; fvlid=1513262212439K3ybIwM5; sessionip=36.149.221.173; sessionid=85EBCD18-EB37-4DBC-88E4-72EC92336CD4%7C%7C2017-12-14+22%3A36%3A52.950%7C%7Cwww.baidu.com; area=110199; ahpau=1; historybbsName4=a-100024%7C%E4%B8%8A%E6%B5%B7%2Co-200042%7C%E8%87%AA%E9%A9%BE%E6%B8%B8%2Co-200225%7C%E5%90%B5%E5%AE%8C%E8%BF%98%E6%98%AF%E6%9C%8B%E5%8F%8B; autoac=92D76CFCB0772AD23D11173BD584EAAE; autotc=C217307368BA9D7AD41FF52269C38D6A; ahpvno=1; Hm_lpvt_9924a05a5a75caf05dbbfb51af638b07=1513418340; CNZZDATA1262640694=431993454-1513259833-https%253A%252F%252Fwww.baidu.com%252F%7C1513415068; sessionvid=EFD39E99-36A5-4BC0-97B4-B11F34DAD959; ref=www.baidu.com%7C0%7C0%7C0%7C2017-12-16+17%3A59%3A00.058%7C2017-12-14+22%3A36%3A52.950; cn_1262640694_dplus=%7B%22distinct_id%22%3A%20%221605574e7e020-0de43f6989305c-5a442916-100200-1605574e7e1262%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201513418365%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201513418365%7D%7D'}
        headers = dict(self.headers.items() | host.items())
        # 获取页面内容
        r = requests.get(url, headers=headers)
        response = html.fromstring(r.text)
        # 匹配ttf font
        cmp = re.compile(",url\('(//.*.ttf)'\) format\('woff'\)")
        rst = cmp.findall(r.text)
        ttf = requests.get("http:" + rst[0], stream=True)
        with open("autohome.ttf", "wb") as pdf:
            for chunk in ttf.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
        # 解析字体库font文件
        font = TTFont('autohome.ttf')
        uniList = font['cmap'].tables[0].ttFont.getGlyphOrder()
        utf8List = [eval("u'\\u" + uni[3:] + "'").encode("utf-8") for uni in uniList[1:]]
        wordList = ['一', '七', '三', '上', '下', '不', '中', '档', '比', '油', '泥', '灯',
                    '九', '了', '二', '五', '低', '保', '光', '八', '公', '六', '养', '内', '冷',
                    '副', '加', '动', '十', '电', '的', '皮', '盘', '真', '着', '路', '身', '软',
                    '过', '近', '远', '里', '量', '长', '门', '问', '只', '右', '启', '呢', '味',
                    '和', '响', '四', '地', '坏', '坐', '外', '多', '大', '好', '孩', '实', '小',
                    '少', '短', '矮', '硬', '空', '级', '耗', '雨', '音', '高', '左', '开', '当',
                    '很', '得', '性', '自', '手', '排', '控', '无', '是', '更', '有', '机', '来']
        # 获取发帖内容
        note = response.cssselect(".tz-paragraph")[0].text_content().encode('utf-8')
        print (note.decode('utf-8'))
        print ('---------------after-----------------')
        for i in range(len(utf8List)):
            # print(type(utf8List[i]),type(wordList[i]))
            note = note.replace(utf8List[i], wordList[i].encode(encoding="utf-8"))
        print (note.decode())

spider = AutoSpider()
spider.getNote()
