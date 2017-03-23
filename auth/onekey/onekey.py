# -*- coding: UTF-8 -*-
'''
Created on 2017年3月8日

@author: dkf6498
'''
from util import authutil
import json
import time  
import Tkinter  # import the Tkinter module
root = Tkinter.Tk()  # create a root window
root.title('一键认证')
Tkinter.Label(root, text='域名 :').grid(row=0, column=0)  # 对Label内容进行 表格式 布局
Tkinter.Label(root, text='usermac :').grid(row=1, column=0)
Tkinter.Label(root, text='userip :').grid(row=2, column=0)  # 对Label内容进行 表格式 布局
Tkinter.Label(root, text='storeId:').grid(row=3, column=0)
Tkinter.Label(root, text='ssid:').grid(row=4, column=0)

#拼接获取code的url
def getCodeUrl(loginurl):
    if int(loginurl.find("Error")) != -1:
        loginLable.config(text="登录重定向错误：" + str(loginurl))
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
    else:
        loginLable.config(text="登录重定向：" + str(loginurl))
    return loginurl;

#拼接获取accesstoken的url
def getAccessTokenUrl(loginurl):
    print type(loginurl),loginurl
    #截取code https://www.baidu.com/?code=352049i0c49f498de0147f7ac3101013&userip=1.1.1.2&portal_server=http://localhost:9980/portal/protocol
    code = loginurl.split("&userip=")[0].split("?code=")[1]
    getAccessTokenUrl = ("http://%s/portal/protocol?response_type=access_token&usermac=%s&userip=%s&code=%s") % (e1.get(),e2.get(),e3.get(),code)
    return getAccessTokenUrl
# 请求code
def onekey():
    passParam = authutil.validateParam(e1.get(),e2.get(),e3.get(),e4.get(),e5.get())
    if passParam == 1:
        accessTokenLable.config(text = "参数不能为空  请检查")
        return
    authutil.updateDefaut("onekey.ini","authurl",e1.get())
    authutil.updateDefaut("onekey.ini","usermac",e2.get())
    authutil.updateDefaut("onekey.ini","userip",e3.get())
    authutil.updateDefaut("onekey.ini","storeId",e4.get())
    authutil.updateDefaut("onekey.ini","ssid",e5.get())
    authurl = ("http://%s/portal/protocol?response_type=code&redirect_uri=http://www.baidu.com&client_id=client2&usermac=%s&userip=%s&userurl=http://www.sina.com&nas_id=%d&ssid=%s") % (e1.get(), e2.get(), e3.get(), int(e4.get()), e5.get())
    res = authutil.do_get(authurl, e1.get())
    # 重定向到登录页面
    loginurl = res.getheader('Location')
    if loginurl.find('60017') != -1:
        loginLable.config(text=("认证失败 " + str(loginurl)))
        return
    #拼接获取code的url
    getcodeUrl = getCodeUrl(loginurl)
    #请求code
    loginLable.config(text="请求 code：" + str(getcodeUrl))
    response = authutil.do_get(getcodeUrl,e1.get())
    loginurl = response.getheader("Location")
    coderesLable.config(text = "请求code返回："+str(loginurl))
    #获取accesstoken url
    accessTokenUrl = getAccessTokenUrl(loginurl)
    accessTokenLable.config(text="请求accesstoken "+str(accessTokenUrl))
    #获取accesstoken
    accessTokenInfo = authutil.do_get(accessTokenUrl,e1.get()).read()
    accessTokenObj = json.loads(accessTokenInfo)
    accesstoken = accessTokenObj["access_token"]
    #获取用户信息
    getUserInfoUrl = ("http://%s/portal/protocol?response_type=userinfo&access_token=%s") % (e1.get(),accesstoken)
    getuserinfoLable.config(text="请求用户信息的url "+str(getUserInfoUrl))
    userinfo = authutil.do_get(getUserInfoUrl,e1.get()).read()
    print userinfo
    if int(userinfo.find("success")) != -1:
        userinfoLable.config(text="认证成功:"+str(userinfo))
    else:
        userinfoLable.config(text="认证失败："+str(userinfo))

# main
v1 = Tkinter.StringVar()  # 设置变量 . 
v2 = Tkinter.StringVar()
v3 = Tkinter.StringVar()  # 设置变量 . 
v4 = Tkinter.StringVar()
v5 = Tkinter.StringVar()

e1 = Tkinter.Entry(root, textvariable=v1)  # 用于储存 输入的内容  
e2 = Tkinter.Entry(root, textvariable=v2)
e3 = Tkinter.Entry(root, textvariable=v3)  # 用于储存 输入的内容  
e4 = Tkinter.Entry(root, textvariable=v4)
e5 = Tkinter.Entry(root, textvariable=v5)

e1.grid(row=0, column=1, padx=10, pady=5)  # 进行表格式布局 . 
e2.grid(row=1, column=1, padx=10, pady=5)
e3.grid(row=2, column=1, padx=10, pady=5)  # 进行表格式布局 . 
e4.grid(row=3, column=1, padx=10, pady=5)
e5.grid(row=4, column=1, padx=10, pady=5)

loginLable = Tkinter.Label(root, text="",wraplength=200)
loginLable.grid(columnspan=2, row=16)
codeLable = Tkinter.Label(root, text="",wraplength=200)
codeLable.grid(columnspan=2, row=17)
coderesLable = Tkinter.Label(root, text="",wraplength=200)
coderesLable.grid(columnspan=2, row=18)
accessTokenLable = Tkinter.Label(root, text="",wraplength=200)
accessTokenLable.grid(columnspan=2, row=19)
getuserinfoLable = Tkinter.Label(root, text="",wraplength=200)
getuserinfoLable.grid(columnspan=2, row=20)
userinfoLable = Tkinter.Label(root, text="",wraplength=200)
userinfoLable.grid(columnspan=2, row=21)

#设置默认值
authurl = authutil.readInit("onekey.ini","authurl")
ssid = authutil.readInit("onekey.ini","ssid") 
storeId = authutil.readInit("onekey.ini","storeId")
usermac = authutil.readInit("onekey.ini","usermac")
userip = authutil.readInit("onekey.ini","userip")

v1.set(authurl)
v2.set(usermac)
v3.set(userip)
v4.set(storeId)
v5.set(ssid)

Tkinter.Button(root, text='认证', width=10, command=onekey).grid(row=6, column=0, sticky=Tkinter.W, padx=10, pady=5)  # 设置 button 指定 宽度 , 并且 关联 函数 , 使用表格式布局 . 
Tkinter.Button(root, text='退出', width=10, command=root.quit).grid(row=6, column=1, sticky=Tkinter.E, padx=10, pady=5)

Tkinter.mainloop()
