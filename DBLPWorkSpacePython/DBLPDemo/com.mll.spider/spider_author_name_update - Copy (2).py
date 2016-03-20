# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#Name    :
#Author : Xueshijun
#MailTo : xueshijun_2010@163.com    / 324858038@qq.com
#QQ     : 324858038
#Blog   : http://blog.csdn.net/xueshijun666
#Created on Sun Mar 06 13:51:34 2016
#Version: 1.0
#-------------------------------------------------------------------------------
from bs4 import BeautifulSoup

from dbconnection import DB 
import tools as mytools
import urllib
import random
import time
import ips as ips

proxylist =  ips.proxylist
db=DB() 
i=110261
step =1
while(i<200300):
    author_list = db.get_author(i,step)
    if(len(author_list)>0):
        for row in author_list:
            error_log =""
            try: 
                print '--------------------------------------------------------------------------------'
                error_log = "%s,%s,%s" % (row['id'],row['author'],row['href'])        
    #            print "error_log:::",error_log 
                '''=====================代理模式===========================  '''  
                proxy = proxylist[random.randint(0,len(proxylist)-1)]
                print "***********************************************************"
                print proxy
                print "***********************************************************" 
                proxies = {'': proxy}  
                opener = urllib.FancyURLopener(proxies)
                f = opener.open(row['href'])
                soup= BeautifulSoup(f.read(), "lxml")   
                '''=====================单机模式===========================
                page = urllib.urlopen(row['href'])   
                soup = BeautifulSoup( page.read(), "lxml")   ''' 
                main = soup.find(id="main")
                name_str=main.find(id="headline").find("span",class_="name primary").get_text()
                result = db.update_author(row['id'],name_str)
                
                #db.close()
                print '[',row['id'],']',result,"@@@",row['author'],"@@@",name_str,'@@@',row['href']
                print '--------------------------------------------------------------------------------'
            except: 
                mytools.log_error("log_error_update_author.log",['',error_log])
        i=i+step
        print "Start : %s" % time.ctime()
        time.sleep(4)
        print "End : %s" % time.ctime()
print "finish!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"