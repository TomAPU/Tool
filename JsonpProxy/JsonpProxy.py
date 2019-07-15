import json
from mitmproxy import ctx
def checkJsonp(s):
    try:
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
        page=(flow.response.content).decode("utf-8",'ignore').strip()
        if checkJsonp(page):
            print("[+]发现JSONP页面")
            print("[+]URL:"+flow.request.pretty_url)
            print("[+]Content:"+page[:500])
            print("-"*30+"\n")
addons = [
    Counter()
]