'''
The beef.py  encapsulated beef api into a python class so that you can use manipulate beef by python.
I didn't implement ALL the feature because I'm so freaaaaaaking lazy.
badly written dirty code. I will be very honored if these code got applied to legal pentest or illegal exciting hacking :) 

这个beef.py用一个python类封装了beef的api，这样你就可以用python来操纵beef了
我没有实现所有的beef api,因为我太他喵的懒了
这些代码实在写的不怎么样，如果有人用来进行合法合规的渗透测试或者惊险刺激的渗透入侵我会非常的荣幸:)
'''
import requests
import json
import time
class ConnectError(Exception):
    def __init__(self,reason):
        print("Failed to connect to beef server.\n Reason:",end='')
        print('reason')
class ModuleNotFount(Exception):
    def __init__(self,modulename):
        print('Not Fount Module:',modulename)
class beefhandle:
    proxies={"http":"127.0.0.1:8080"}
    __beef_token=''
    __beef_address=''
    __beef_port=''
    __beef_protocol=''
    __beef_module_data=dict()
    def  __init__(self,username,password,addr='127.0.0.1',port='3000',ssl=False,timeout=3):
        '''
        Connect to a beef server by username and password
        '''
        if ssl:
            protocol='https://'
        else:
            protocol='http://'
        headers={"Content-Type": "application/json"}
        url=protocol+addr+":"+str(port)+"/api/admin/login"
        credential=json.dumps({"username":username,"password":password})
        try:
            r=requests.post(url=url,headers=headers,data=credential,timeout=timeout)
        except TimeoutError:
            raise ConnectError('timeout')
        if r.status_code=='401':
            raise ConnectError('invalid credential')
        #initialization
        self.__beef_protocol=protocol
        self.__beef_address=addr
        self.__beef_port=str(port)
        self.__beef_token=json.loads(r.text)['token']

    def __baseurl(self):
        '''
        return type:str
        return  protocol://address:port
        '''
        return self.__beef_protocol+self.__beef_address+":"+self.__beef_port

    def GetOnlineBrowsers(self,detail=True):
        '''
        return type:list
        Fetch data of hooked browsers.
        in default cases,the function will return details of hooked online browsers
        if detail is False , the function will  return  sessionid only
        '''
        url=self.__baseurl()+"/api/hooks"+"?token="+self.__beef_token
        page=requests.get(url=url).text
        j=json.loads(page)['hooked-browsers']['online']
        sessions=list()
        for key in j:
            if detail:
                sessions.append(j[key])
            else:
                sessions.append(j[key]['session'])
        return sessions
    def GetBrowserDetail(self,sessionid):
        '''
        return type:json
        Fetch browser detail by 
        '''
        url=self.__baseurl()+'/api/hooks/'+sessionid+"?token="+self.__beef_token
        r=requests.get(url=url)
        if r.status_code==200:
            return json.loads(r.text)
        return json.loads({})

    def GetModuleIDByName(self,name):
        '''
        return type:str
        get module id by command name
        '''
        if  self.__beef_module_data==dict():
            url=self.__baseurl()+'/api/modules'+"?token="+self.__beef_token
            page=requests.get(url=url).text
            j=json.loads(page)
            for key in j:
                self.__beef_module_data[j[key]['name']]=j[key]
        if name in self.__beef_module_data:
            return str(self.__beef_module_data[name]['id'])
        raise ModuleNotFoundError(name)

    def GetCommandResult(self,sessionid,moduleid,commandid,timeout=0):
        '''
        return type:str or None, based on whether the command is done
        given sessionid moduleid commandid,fetch the command result
        the function will try to fetch command result every 0.2 seconds until the result  is fetched or timeout
        if timeout is zero,the function will fetch result once
        '''
        url=self.__baseurl()+"/api/modules/"+sessionid+"/"+moduleid+'/'+commandid+"?token="+self.__beef_token
        page=requests.get(url=url).text
        starttime=time.time()
        while page=="{}" and time.time()-starttime<timeout:
            time.sleep(0.2)
            page=requests.get(url=url).text
        if page=="{}":
            return None
        return json.loads(json.loads(page)['0']['data'])['data']
    
    def ExecuteCommand(self,sessionid,command_name,cmd_parameters=None,wait=True,timeout=10):
        '''
        return type:str or list ,based on your 'wait' parameter
        provide sessionid,command_name and cmd_parameters to exeute command on a certain session
        if wait is False then the function will return  (sessionid,moduleid,commandid) so that you can fetch command result by your self
        if wait is true,you should set a timeout (default=10) to wait for the result,and the string type result will be returned.
        '''
        if not cmd_parameters:
            cmd_parameters=dict()
        cmd_parameters=json.dumps(cmd_parameters)
        moduleid=self.GetModuleIDByName(command_name)
        headers={"Content-Type": "application/json"}
        url=self.__baseurl()+"/api/modules/"+sessionid+"/"+moduleid+"?token="+self.__beef_token
        page=requests.post(url=url,headers=headers,data=cmd_parameters).text
        j=json.loads(page)
        commandid=j['command_id']
        if not wait:
            return list((sessionid,moduleid,commandid))
        result=self.GetCommandResult (sessionid,moduleid,commandid,timeout)
        return result