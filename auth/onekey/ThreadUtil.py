# -*- coding: UTF-8 -*-
'''
Created on 2017年3月8日

@author: dkf6498
'''
from util import authutil
import json
import time  
import Tkinter  # import the Tkinter module
import thread

root = Tkinter.Tk()  # create a root window
root.title('一键认证')
Tkinter.Label(root, text='域名 :').grid(row=0, column=0) 
Tkinter.Label(root, text='storeId :').grid(row=1, column=0)  
Tkinter.Label(root, text='ssid:').grid(row=2, column=0)
Tkinter.Label(root, text='并发数:').grid(row=3, column=0)

#拼接获取code的url
def getCodeUrl(loginurl):
    if int(loginurl.find("Error")) != -1:
        return 'error'
    elif loginurl.find("?code=") == -1:
        # 没找到code  获取param
        templateId = loginurl.split("&location=")[0].split("templateId=")[1]
        location = loginurl.split("&redirect_uri=")[0].split("&location=")[1]
        redirect_uri = loginurl.split("&nas_id=")[0].split("&redirect_uri=")[1]
        nas_id = loginurl.split("&ssid=")[0].split("&nas_id=")[1]
        ssid = loginurl.split("&usermac=")[0].split("&ssid=")[1]
        usermac = loginurl.split("&userip=")[0].split("&usermac=")[1]
        userip = loginurl.split("&userurl=")[0].split("&userip=")[1]
        userurl = loginurl.split("&apmac=")[0].split("&userurl=")[1]
        apmac = loginurl.split("&_ts")[0].split("&apmac=")[1]
        # 请求code
        getcodeUrl = ("http://%s/portal/login?operateType=1&templateId=%s&location=%s&redirect_uri=%s&nas_id=%s&ssid=%s&usermac=%s&userip=%s&userurl=%s&apmac=%s&_ts=%s") % (e1.get(), templateId, location, redirect_uri, nas_id, ssid, usermac, userip, userurl, apmac, int(time.time()))
        return getcodeUrl
    return loginurl;

#拼接获取accesstoken的url
def getAccessTokenUrl(loginurl,authurl,usermac,userip,storeId,ssid):
    #截取code https://www.baidu.com/?code=352049i0c49f498de0147f7ac3101013&userip=1.1.1.2&portal_server=http://localhost:9980/portal/protocol
    code = loginurl.split("&userip=")[0].split("?code=")[1]
    getAccessTokenUrl = ("http://%s/portal/protocol?response_type=access_token&usermac=%s&userip=%s&code=%s") % (e1.get(),usermac,userip,code)
    return getAccessTokenUrl
# 请求code
def onekeytest(authurl,usermac,userip,storeId,ssid):
    passParam = authutil.validateParam(authurl,usermac,userip,storeId,ssid)
    if passParam == 1:
        return 'error'
    authutil.updateDefaut("onekeyThread.ini","authurl",authurl)
    authutil.updateDefaut("onekeyThread.ini","storeId",storeId)
    authutil.updateDefaut("onekeyThread.ini","ssid",ssid)
    authurl = ("http://%s/portal/protocol?response_type=code&redirect_uri=http://www.baidu.com&client_id=client2&usermac=%s&userip=%s&userurl=http://www.sina.com&nas_id=%d&ssid=%s") % (authurl,usermac,userip,storeId, ssid)
    res = authutil.do_get(authurl, e1.get())
    # 重定向到登录页面
    loginurl = res.getheader('Location')
    if loginurl.find('60017') != -1:
        return 'error'
    #拼接获取code的url
    getcodeUrl = getCodeUrl(loginurl)
    print "getcodeUrl is ",getcodeUrl
    #请求code
    response = authutil.do_get(getcodeUrl,e1.get())
    loginurl = response.getheader("Location")
    print "Location url is",loginurl
    #获取accesstoken url
    accessTokenUrl = getAccessTokenUrl(loginurl,authurl,usermac,userip,storeId,ssid)
    print "get accessToken url is ",accessTokenUrl
    #获取accesstoken
    accessTokenInfo = authutil.do_get(accessTokenUrl,e1.get()).read()
    print accessTokenInfo
    accessTokenObj = json.loads(accessTokenInfo)
    accesstoken = accessTokenObj["access_token"]
    #获取用户信息
    getUserInfoUrl = ("http://%s/portal/protocol?response_type=userinfo&access_token=%s") % (e1.get(),accesstoken)
    userinfo = authutil.do_get(getUserInfoUrl,e1.get()).read()
    print userinfo
    if int(userinfo.find("Success")) != -1:
        print 'ok'
        return 'ok'
    else:
        print 'error'
        return 'error'
        
# main
v1 = Tkinter.StringVar()  # 设置变量 . 
v2 = Tkinter.StringVar()
v3 = Tkinter.StringVar()  # 设置变量 . 
v4 = Tkinter.StringVar()

e1 = Tkinter.Entry(root, textvariable=v1)  # 用于储存 输入的内容  
e2 = Tkinter.Entry(root, textvariable=v2)
e3 = Tkinter.Entry(root, textvariable=v3)  # 用于储存 输入的内容  
e4 = Tkinter.Entry(root, textvariable=v4)

e1.grid(row=0, column=1, padx=10, pady=5)  # 进行表格式布局 . 
e2.grid(row=1, column=1, padx=10, pady=5)
e3.grid(row=2, column=1, padx=10, pady=5)  # 进行表格式布局 . 
e4.grid(row=3, column=1, padx=10, pady=5)

#设置默认值
authurl = authutil.readInit("onekeyThread.ini","authurl")
ssid = authutil.readInit("onekeyThread.ini","ssid") 
storeId = authutil.readInit("onekeyThread.ini","storeid")
threadNo = authutil.readInit("onekeyThread.ini","threadNo")

v1.set(authurl)
v2.set(storeId)
v3.set(ssid)
v4.set(threadNo)


def threadAuth():
    failSum = 0;
    authurl = e1.get()
    storeId = e2.get()
    ssid = e3.get()
    threadNo = e4.get()
    maclist = authutil.getMACList(int(threadNo))
    iplist = authutil.getIpList(int(threadNo))
    for i in range(0,int(threadNo)):
        result = ""
        thread.start_new_thread(onekeytest, (authurl,maclist[i],iplist[i],int(storeId),ssid) )
        if result == 'error':
            failSum = failSum + 1
    print '失败次数'+str(failSum)

Tkinter.Button(root, text='认证', width=10, command=threadAuth).grid(row=6, column=0, sticky=Tkinter.W, padx=10, pady=5)  # 设置 button 指定 宽度 , 并且 关联 函数 , 使用表格式布局 . 
Tkinter.Button(root, text='退出', width=10, command=root.quit).grid(row=6, column=1, sticky=Tkinter.E, padx=10, pady=5)

Tkinter.mainloop()
