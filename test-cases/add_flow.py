# coding=utf-8

import os,unittest,time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import unittest, time, re
import yaml
import uuid
from pprint import pprint
import sys
sys.path.append("..")
import base

DEBUG = True

class add_flow(unittest.TestCase):
    def loadInput(self, cfg):
        """load input data from chuanyue.yaml"""
        try:
            stream = open(cfg['test_input_path']+'/chuanyue.yaml', 'r')
        except Exception, e:
            print "cannot open " + cfg['test_input_path']+'/chuanyue.yaml'
            raise e
        data = yaml.load(stream)
        return data

    def setUp(self):
        self.cfg = testvars
        iedriver = "D:\python27\IEDriverServer.exe"
        os.environ["webdriver.ie.driver"] = iedriver
        self.driver = webdriver.Ie(iedriver)
        self.driver.implicitly_wait(self.cfg['implicit_wait'])
        self.base_url = self.cfg['base_url']
        self.data = self.loadInput(self.cfg)
    
    def test_add_flow(self):
        dr = self.driver
        dr.get(self.base_url)
        #登录
        base.login(dr,self.cfg['admin'],self.cfg['password'])
        
        #获取当前window句柄
        now_handle = dr.current_window_handle
        dr.switch_to.frame("indexFrame")
        dr.switch_to.frame("MenuFrame")        
        
        #新增流程
        dr.find_element_by_xpath("//div[@id='tree']/ul/li/ul/li/ul/li[9]/a").click()
        dr.switch_to.default_content()
        dr.switch_to.frame("indexFrame")
        dr.switch_to.frame("PageFrame")
        dr.find_element_by_id("ctl00_cntGrid1_hlkDefineGeneralFlow").click()
        dr.find_element_by_id("ctl00_cntGrid1_cmdVmlAdd").click()

        #填写标题并新建        
        t = time.strftime('_%m%d_%H:%M',time.localtime(time.time()))
        dr.find_element_by_id("ctl00_cntForm_txtName").send_keys("TestFlow"+t)
        Select(dr.find_element_by_id("ctl00_cntForm_drpModName")).select_by_visible_text(u"通用流程")
        dr.find_element_by_id("ctl00_cntButton_cmdSaveList").click()


        #定义步骤 

        #添加通知执行步骤                         
        self.add_step(u"通知执行")

        dr.switch_to.window(now_handle)
        dr.switch_to.default_content()
        dr.switch_to.frame("indexFrame")
        dr.switch_to.frame("PageFrame")

        #添加审批步骤             
        self.add_step(u"审批")      
       
        #跳转回原窗口
        dr.switch_to.window(now_handle)
        dr.switch_to.default_content()
        dr.switch_to.frame("indexFrame")
        dr.switch_to.frame("PageFrame")

        #添加权限对象
        dr.find_element_by_id("ctl00_cntTitle_EditTab1_cmdTab2").click()
        dr.find_element_by_id("ctl00_cntForm_ioCustomRightSet1_cmdRightAdd").click()
        dr.find_element_by_id("ctl00_cntForm_radType_0").click()
        dr.find_element_by_id("ctl00_cntButton_cmdNext").click()
        Select(dr.find_element_by_id("ctl00_cntForm_lstDep")).select_by_value("1")
        dr.find_element_by_id("ctl00_cntForm_cmdAdd").click()
        dr.find_element_by_id("ctl00_cntButton_cmdFinish").click()

        #保存退出
        dr.find_element_by_id("ctl00_cntButton_cmdSaveExi").click()


        #验证流程
        dr.find_element_by_id("ctl00_cntQuery_IoFieldQuery1_txtSimple").send_keys("TestFlow"+t)
        dr.find_element_by_id("ctl00_cntQuery_cmdQuery").click()
        dr.find_element_by_xpath("//table[@id='ctl00_cntGrid2_dgdData']/tbody/tr[2]/td[2]/a").click()   

        fstep = dr.find_element_by_xpath("//table[@id='ctl00_cntForm_dgdStep']/tbody/tr[3]/td[1]").text
        sstep = dr.find_element_by_xpath("//table[@id='ctl00_cntForm_dgdStep']/tbody/tr[4]/td[1]").text

        self.assertEqual(u"通知执行",fstep)
        self.assertEqual(u"审批",sstep)
        dr.save_screenshot(self.cfg['test_output_path']+u"screenshot\流程1.png")


    def tearDown(self):        
        self.driver.quit()
        

    def add_step(self,step):
        dr = self.driver
        dr.find_element_by_id("ctl00_cntForm_cmdAdd").click()
        sleep(1)
        dr.switch_to.window("selre")
        dr.find_element_by_id("ctl00_cntForm_txtStepName").send_keys(step)
        Select(dr.find_element_by_id("ctl00_cntForm_drpActionType")).select_by_visible_text(step)
        #选人
        dr.find_element_by_id("ctl00_cntForm_cmdSelAssgn").click()
        sleep(1)
        dr.switch_to.window("assgn")       
        dr.find_element_by_id("ctl00_cntForm_radType_1").click()
        Select(dr.find_element_by_id("ctl00_cntForm_dropBranch")).select_by_value("1")
        Select(dr.find_element_by_id("ctl00_cntForm_lstEmp")).select_by_visible_text(u"-执行时替换-")
        dr.find_element_by_id("ctl00_cntForm_cmdAdd").click()        
        dr.find_element_by_id("ctl00_cntButton_cmdOK").click()
        dr.switch_to.window("selre")
        dr.find_element_by_id("ctl00_cntButton_cmdSaveExi").click() 

        

if __name__ == "__main__":
    unittest.main()
