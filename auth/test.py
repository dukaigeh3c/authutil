# -*- coding: UTF-8 -*-
'''
Created on 2017��3��22��

@author: dkf6498
'''
import urllib
import re 
   
def getImg(url):
    x = 0
    for i in range(1, 31):
        headers = {                     #伪装浏览器
          'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                 ' Chrome/32.0.1700.76 Safari/537.36'
        }
        url = url + str(i)
        page = urllib.urlopen(url)
        html = page.read()
        reg = r'src=("https://.*?\.gif") | src=("https://.*?\.png") | src="(https://.*?\.jpg)" |src=("https://.*?\.img")'
        imgre = re.compile(reg)
        imglist = re.findall(imgre,html)
        for imgurl in imglist:
            if str(imgurl).find('jpg') != -1:
                if str(imgurl).find('http') != -1 :
                    URL= 'http'+(str(imgurl).split('.jpg')[0].split('http')[1])+'.jpg'
                    print URL
                    try:
                        urllib.urlretrieve(URL,'C:\Users\dkf6498\Desktop\download\%s.jpg' % x)
                        x+=1
                    except:
                        print '错误的图片地址'+str(URL)
            elif str(imgurl).find('png') != -1:
                if str(imgurl).find('http') != -1 :
                    URL = 'http'+(str(imgurl).split('.png')[0].split('http')[1])+'.png'
                    print URL
                    try:
                        urllib.urlretrieve(URL,'C:\Users\dkf6498\Desktop\download\%s.png' % x)
                        x+=1
                    except:
                        print '错误的图片地址'+str(URL)
            elif str(imgurl).find('gif') != -1:
                if str(imgurl).find('http') != -1 :
                    URL = 'http'+(str(imgurl).split('.gif')[0].split('http')[1])+'.gif'
                    print URL
                    try:
                        urllib.urlretrieve(URL,'C:\Users\dkf6498\Desktop\download\%s.gif' % x)
                        x+=1
                    except:
                        print '错误的图片地址'+str(URL)
            elif str(imgurl).find('img') != -1:
                if str(imgurl).find('http') != -1 :
                    URL = 'http'+(str(imgurl).split('.img')[0].split('http')[1])+'.img'
                    print URL
                    try:
                        urllib.urlretrieve(URL,'C:\Users\dkf6498\Desktop\download\%s.img' % x)
                        x+=1
                    except:
                        print '错误的图片地址'+str(URL)
#调用  
getImg('https://tieba.baidu.com/p/2072572551?pn=')
