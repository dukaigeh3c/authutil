# -*- coding: UTF-8 -*-
'''
Created on 2017年3月8日

@author: dkf6498
'''
import json
import base64
import Tkinter  # import the Tkinter module

from util import authutil

root = Tkinter.Tk()  # create a root window
root.title('微信连wifi认证')
Tkinter.Label(root, text='域名 :').grid(row=0, column=0)  # 对Label内容进行 表格式 布局
Tkinter.Label(root, text='usermac :').grid(row=1, column=0)
Tkinter.Label(root, text='userip :').grid(row=2, column=0)  # 对Label内容进行 表格式 布局
Tkinter.Label(root, text='storeId:').grid(row=3, column=0)
Tkinter.Label(root, text='ssid:').grid(row=4, column=0)
Tkinter.Label(root, text='openid:').grid(row=5, column=0)
Tkinter.Label(root, text='tid:').grid(row=6, column=0)

#拼接获取accesstoken的url
def getAccessTokenUrl(loginurl):
    print type(loginurl),loginurl
    #截取code https://www.baidu.com/?code=352049i0c49f498de0147f7ac3101013&userip=1.1.1.2&portal_server=http://localhost:9980/portal/protocol
    code = loginurl.split("&userip=")[0].split("?code=")[1]
    getAccessTokenUrl = ("http://%s/portal/protocol?response_type=access_token&usermac=%s&userip=%s&code=%s") % (e1.get(),e2.get(),e3.get(),code)
    return getAccessTokenUrl

def doAuthToWeixinServer(loginurl):
    print loginurl
    if int(loginurl.find("Error")) != -1:
        openWxLable.config(text="登录重定向错误：" + str(loginurl))
    elif loginurl.find("?code=") != -1:
        # 找到code  直接返回
        return loginurl
    else:
        templateId = loginurl.split("&location=")[0].split("templateId=")[1]
        redirect_uri = loginurl.split("&nas_id=")[0].split("&redirect_uri=")[1]
        nas_id = loginurl.split("&ssid=")[0].split("&nas_id=")[1]
        ssid = loginurl.split("&usermac=")[0].split("&ssid=")[1]
        usermac = loginurl.split("&userip=")[0].split("&usermac=")[1]
        userip = loginurl.split("&userurl=")[0].split("&userip=")[1]
        userurl = loginurl.split("&apmac=")[0].split("&userurl=")[1]
        authUrl = ("http://%s/portal/wifilogin.jsp?nas_id=%s&redirect_uri=%s&ssid=%s&templateId=%s&userip=%s&usermac=%s&userurl=%s") % (e1.get(),nas_id,redirect_uri,ssid,templateId,userip,usermac,userurl)
        print authUrl
        openWxLable.config(text=("拉起微信客戶端的url " + str(authUrl)))
        #向authurl發起認證
        data=("nas_id=%s&redirect_uri=%s&ssid=%s&userip=%s&usermac=%s") % (nas_id,redirect_uri,ssid,userip,usermac)
        dataLable.config(text = "未加密的data : " + str(data))
        #转成bytes string
        bytesString = str(data).encode(encoding="utf-8")
        #base64 编码
        extend = base64.b64encode(bytesString)
        auth_url=("http://%s/weixinwifi/clientauth?openId=%s&tid=%s&extend=%s") % (e1.get(),e6.get(),e7.get(),extend)
        #发送认证请求
        print auth_url
        res = authutil.do_get(auth_url,str(e1.get()))
        return res.getheader('Location')

# 请求code
def wechat():
    passParam = authutil.validateParam(e1.get(),e2.get(),e3.get(),e4.get(),e5.get(),e6.get(),e7.get())
    if passParam == 1:
        accessTokenLable.config(text = "参数不能为空  请检查")
        return
    #修改默认值
    authutil.updateDefaut('authdata.ini',"authurl",e1.get())
    authutil.updateDefaut('authdata.ini',"usermac",e2.get())
    authutil.updateDefaut('authdata.ini',"userip",e3.get())
    authutil.updateDefaut('authdata.ini',"storeId",e4.get())
    authutil.updateDefaut('authdata.ini',"ssid",e5.get())
    authutil.updateDefaut('authdata.ini',"openId",e6.get())
    authutil.updateDefaut('authdata.ini',"tid",e7.get())
    authurl = ("http://%s/portal/protocol?response_type=code&redirect_uri=http://www.baidu.com&client_id=client2&usermac=%s&userip=%s&userurl=http://www.sina.com&nas_id=%d&ssid=%s") % (e1.get(), e2.get(), e3.get(), int(e4.get()), e5.get())
    res = authutil.do_get(authurl, e1.get())
    # 重定向到登录页面
    loginurl = res.getheader('Location')
    print loginurl
    if loginurl.find('60017') != -1:
        openWxLable.config(text=("认证失败 " + str(loginurl)))
        return
    redirect_uri = doAuthToWeixinServer(loginurl)
    codeLable.config(text=("含有code的url "+str(redirect_uri)))
    #获取accesstoken url
    accessTokenUrl = getAccessTokenUrl(redirect_uri)
    accessTokenLable.config(text=("请求accesstoken : "+str(accessTokenUrl)))
    #获取accesstoken
    accessTokenInfo = authutil.do_get(accessTokenUrl,e1.get()).read()
    accessTokenObj = json.loads(accessTokenInfo)
    accesstoken = accessTokenObj["access_token"]
    #获取用户信息
    getUserInfoUrl = ("http://%s/portal/protocol?response_type=userinfo&access_token=%s") % (e1.get(),accesstoken)
    getuserinfoLable.config(text = ("请求用户信息的url "+str(getUserInfoUrl)))
    userinfo = authutil.do_get(getUserInfoUrl,e1.get()).read()
    print userinfo
    if int(userinfo.find("username")) != -1:
        userinfoLable.config(text=("上线成功  用户信息 ：" + str(userinfo)))
    else:
        userinfoLable.config(text=("上线失败 "+str(userinfo)))

# main
v1 = Tkinter.StringVar()  # 设置变量 . 
v2 = Tkinter.StringVar()
v3 = Tkinter.StringVar()  # 设置变量 . 
v4 = Tkinter.StringVar()
v5 = Tkinter.StringVar()
v6 = Tkinter.StringVar()
v7 = Tkinter.StringVar()

e1 = Tkinter.Entry(root, textvariable=v1)  # 用于储存 输入的内容  
e2 = Tkinter.Entry(root, textvariable=v2)
e3 = Tkinter.Entry(root, textvariable=v3)  # 用于储存 输入的内容  
e4 = Tkinter.Entry(root, textvariable=v4)
e5 = Tkinter.Entry(root, textvariable=v5)
e6 = Tkinter.Entry(root, textvariable=v6)
e7 = Tkinter.Entry(root, textvariable=v7)

e1.grid(row=0, column=1, padx=10, pady=5)  # 进行表格式布局 . 
e2.grid(row=1, column=1, padx=10, pady=5)
e3.grid(row=2, column=1, padx=10, pady=5)  # 进行表格式布局 . 
e4.grid(row=3, column=1, padx=10, pady=5)
e5.grid(row=4, column=1, padx=10, pady=5)
e6.grid(row=5, column=1, padx=10, pady=5)
e7.grid(row=6, column=1, padx=10, pady=5)

tipsLable = Tkinter.Label(root,text='tips: openid和tid可以通过oasisrdauth.h3c.com/portal/getOpenId.jsp?appId={appid}&shopId={shopiD}获取',wraplength=200)
tipsLable.grid(columnspan=2, row=15)
openWxLable = Tkinter.Label(root, text="",wraplength=200)
openWxLable.grid(columnspan=2, row=16)
dataLable = Tkinter.Label(root, text="",wraplength=200)
dataLable.grid(columnspan=2, row=17)
codeLable = Tkinter.Label(root, text="",wraplength=200)
codeLable.grid(columnspan=2, row=18)
accessTokenLable = Tkinter.Label(root, text="",wraplength=200)
accessTokenLable.grid(columnspan=2, row=19)
getuserinfoLable = Tkinter.Label(root, text="",wraplength=200)
getuserinfoLable.grid(columnspan=2, row=20)
userinfoLable = Tkinter.Label(root, text="",wraplength=200)
userinfoLable.grid(columnspan=2, row=21)

#设置默认值
authurl = authutil.readInit('authdata.ini',"authurl")
openId = authutil.readInit('authdata.ini',"openId")
tid = authutil.readInit('authdata.ini',"tid")
ssid = authutil.readInit('authdata.ini',"ssid") 
storeId = authutil.readInit('authdata.ini',"storeId")
usermac = authutil.readInit('authdata.ini',"usermac")
userip = authutil.readInit('authdata.ini',"userip")

v1.set(authurl)
v2.set(usermac)
v3.set(userip)
v4.set(storeId)
v5.set(ssid)
v6.set(openId)
v7.set(tid)

Tkinter.Button(root, text='认证', width=10, command=wechat).grid(row=8, column=0, sticky=Tkinter.W, padx=10, pady=5)  # 设置 button 指定 宽度 , 并且 关联 函数 , 使用表格式布局 . 
Tkinter.Button(root, text='退出', width=10, command=root.quit).grid(row=8, column=1, sticky=Tkinter.E, padx=10, pady=5)

Tkinter.mainloop()
