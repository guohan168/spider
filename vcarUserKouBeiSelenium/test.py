


import re,io
import requests


from fontTools.ttLib import TTFont

_pat_font_content = re.compile('myFont; src: url\("data:application/octet-stream;base64,(.+?)"')
_pat_font = re.compile('&#x[0-9a-f]{4}')

maps = {}


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Host': 'www.shixiseng.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}


def get_font_regx(content):
    if content in maps:
        return maps[content]
    ctx = content.encode("utf-8").decode('utf-8')
    font = TTFont(ctx)
    mappings = {}
    for k, v in font.getBestCmap().items():
        if v.startswith('uni'):
            mappings['&#x{:x}'.format(k)] = chr(int(v[3:], 16))
        else:
            mappings['&#x{:x}'.format(k)] = v

def callback(regx):
    return mappings.get(regx.group(0), regx.group(0))
maps[content] = callback
return callback

if __name__ == '__main__':
    resp = requests.get('https://www.shixiseng.com/interns?k=python&p=1', headers=headers)
    content = _pat_font_content.search(resp.text).group(1)
    callback = get_font_regx(content)
    text = _pat_font.sub(callback, resp.text)
    print(text)
