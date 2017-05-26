# -*- coding: UTF-8 -*-
'''
Created on 2017��3��18��

@author: dkf6498
'''
import ConfigParser
import urllib2
import httplib
import random
import string

def readInit(fileName,param):
    config = ConfigParser.ConfigParser()
    config.readfp(open(fileName))
    return config.get("ZIP",param)
   
def updateDefaut(fileName,param,newparam):
    config = ConfigParser.ConfigParser()
    config.read(fileName)
    config.set("ZIP", param, newparam) #这样md5就从1234变成kingsoft了
    config.write(open(fileName, "r+"))
    
def printLog(message):
    config = ConfigParser.ConfigParser()
    config.read("thread.ini")
    config.set("LOG",message)
    config.write(open("thread.log", "w"))
# 发送get请求
def do_get(authurl, domain):
    conn = httplib.HTTPConnection(domain)
    conn.request(method="GET", url=authurl) 
    response = conn.getresponse()
    return response
    
# 发送post请求
# params {'ServiceCode':'aaaa','b':'bbbbb'}
def do_post(authurl, params):
    req = urllib2.Request(url=authurl, data=params)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    print "response is :", res;
    return res

def validateParam(*params):
    passParam = 0
    for param in params:
        if param == '':
            passParam = 1
    return passParam

def getMACList(size):
    index = 0
    MacList = [1]*size
    while 1:
        mac = getMac()
        while mac in MacList:
            mac = getMac()
        MacList[index] = mac
        if index == size-1:
            return MacList
        index = index+1
def getMac():
    mac = ''
    for latter in range(1,6):
        if latter == 5:
            mac += string.join(random.sample(['A','B','C','D','E','F','0','1','2','3','4','5','6','7','8','9'], 2)).replace(" ","")
        else:
            mac += string.join(random.sample(['A','B','C','D','E','F','0','1','2','3','4','5','6','7','8','9'], 2)).replace(" ","") + '-'
    return mac;

def getIp():
    ip = ''
    for latter in range(1,5):
        if latter == 4:
            ip += string.join(random.sample(['0','1','2','3','4','5','6','7','8','9'], 3)).replace(" ","")
        else:
            ip += string.join(random.sample(['0','1','2','3','4','5','6','7','8','9'], 3)).replace(" ","") + '.'
    return ip;
def getIpList(size):
    index = 0
    ipList = [1]*size
    while 1:
        ip = getIp()
        while ip in ipList:
            ip = getMac()
        ipList[index] = ip
        if index == size-1:
            return ipList
        index = index+1
