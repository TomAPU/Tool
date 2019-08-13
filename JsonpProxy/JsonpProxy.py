import json
from mitmproxy import ctx
def checkJsonp(s):
    try:
        if s[-1]==';':
            s=s[:-1]
        if s[-1]!=')':
            return False
        json.loads(s[s.index('(')+1:-1])
        return True
    except Exception as err:
        #print(err)
        return False
class Counter:
    def __init__(self):
        pass

    def response(self, flow):
        page=(flow.response.content)
        page="".join(map(chr, page))
        url=flow.request.pretty_url.lower()
        #由于jsonp本质上是通过js的跨域实现的，想要精确写出一个checkjsonp比登天还难，所以在url里面也加入了检测，可能会带来一些误报
        if checkJsonp(page) or 'callback' in  url or 'cbk' in url:
            print("[+]发现（疑似）JSONP页面")
            print("[+]URL:"+flow.request.pretty_url)
            print("[+]Content:"+page[:500])
            print("-"*30+"\n")
addons = [
    Counter()
]
