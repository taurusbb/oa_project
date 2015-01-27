# coding=utf-8
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.support.ui import Select


     
        
def login(dr1,loginid,pwd):
    dr = dr1
    dr.find_element_by_name("txtloginid").clear()
    dr.find_element_by_name("txtloginid").send_keys(loginid)
    dr.find_element_by_name("txtpwd").send_keys(pwd)
    dr.find_element_by_id("ok").submit()

def choose_emp(dr2,emp):
    dr = dr2
    Select(dr.find_element_by_id("ctl00_cntForm_lstEmp")).select_by_visible_text(emp)
    dr.find_element_by_id("ctl00_cntForm_cmdAdd").click()
    dr.find_element_by_id("ctl00_cntButton_cmdOK").click()

def ExeMgr():
    appPath = "D:/Python27/testcase/auto.exe"
    pid = None
    '''
        启动应用程序
    '''
    #判断应用程序路径是否存在
    if(os.path.exists(appPath)):
        p = subprocess.Popen(appPath)
        pid = p.pid
        if pid is None:
            return False
        return True
    else:
        print(u'应用程序路径'+appPath+u'不存在')

