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

class add_shouwen(unittest.TestCase):
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
    
    def test_add_shouwen(self):

        dr = self.driver
        dr.get(self.base_url)
        #登录
        base.login(dr,self.cfg['username'],self.cfg['password'])
        
        name = u"收文" + '-' + \
        time.strftime('%m%d-%H:%M:%S', time.localtime(time.time()))
        zihao = "zihao1"        
        flowname = u"new收文测试"
        sendgov = u"机关1"
        lwdanwei = u"来文单位1"

########################################新建收文####################################################
        # WebDriverWait(dr, 10).until(lambda the_driver: the_driver.find_element_by_id('indexFrame').is_displayed())        
        dr.switch_to.frame("indexFrame")
        dr.find_element_by_id("imgCloseRemind").click()
        dr.switch_to.frame("MenuFrame")
        # 新增收文
        # 点击公文管理节点
        dr.find_element_by_xpath("//div[@id='tree']/ul/li/ul/li[1]/ul/li[7]/span").click()        
        dr.find_element_by_xpath("//div[@id='tree']/ul/li/ul/li/ul/li[7]/ul/li[1]/a").click()

        dr.switch_to.default_content()
        dr.switch_to.frame("indexFrame")
        dr.switch_to.frame("PageFrame")

        dr.find_element_by_id("ctl00_cntGrid1_hypAdd").click()   

        # 填写标题
        dr.find_element_by_id("ctl00_cntForm_txtTitle").send_keys(name)
        dr.find_element_by_id("ctl00_cntForm_txtZihao").send_keys(zihao)
        Select(dr.find_element_by_id("ctl00_cntForm_FlowSelFlow1_drpFlow")).select_by_visible_text(flowname)
        dr.find_element_by_id("ctl00_cntForm_txtFromGov").send_keys(lwdanwei)
        Select(dr.find_element_by_id("ctl00_cntForm_drpDocReNumberSet")).select_by_index(1)
        # WebDriverWait(dr, 10).until(lambda the_driver: the_driver.find_element_by_id('ctl00_cntForm_drpDocReUnitWord').is_displayed())
        Select(dr.find_element_by_id("ctl00_cntForm_drpDocReUnitWord")).select_by_index(1)
        

        first_handle = dr.current_window_handle #获取当前窗口句柄
        dr.find_element_by_id("ctl00_cntForm_hypKeyWord").click()
        sleep(2)
        dr.switch_to.window("SelBaseDic") 
        webdriver.ActionChains(dr).double_click(dr.find_element_by_id("ctl00_cntForm_dgdData_ctl02_Label2")).perform()       
        

        dr.switch_to.window(first_handle)
        dr.switch_to.default_content()
        dr.switch_to.frame("indexFrame")
        dr.switch_to.frame("PageFrame")

        # WebDriverWait(dr, 10).until(lambda the_driver: the_driver.find_element_by_id('ctl00_cntButton_FlowAction1_cmdSubmit').is_displayed())
        # 提交
        dr.find_element_by_id("ctl00_cntButton_FlowAction1_cmdSubmit").click()
        # WebDriverWait(dr, 10).until(lambda the_driver: the_driver.find_element_by_id('ctl00_cntForm_lstEmp').is_displayed())

        # 下一步执行人
        base.choose_emp(dr,u"-流程申请人-")

        # 验证新建发文
        dr.save_screenshot(u"screenshot\新建收文.png")
        

####################################################################################################




########################################流程处理####################################################
    # def test_process_fawen(self):
    #     dr = self.driver
        dr.switch_to.default_content()
        dr.switch_to.frame("indexFrame")
        dr.switch_to.frame("MenuFrame")
        # 查询待办公文
        # 点击我的批复节点
        dr.find_element_by_xpath("//div[@id='tree']/ul/li/ul/li[2]/span").click()        
        dr.find_element_by_xpath("//div[@id='tree']/ul/li/ul/li[2]/ul/li[2]/a/span").click()

        dr.switch_to.default_content()
        dr.switch_to.frame("indexFrame")        
        dr.switch_to.frame("PageFrame")
        #点击显示全部流程
        dr.find_element_by_id("ctl00_cntGrid2_TreeView1t0").click()
        #点击第一条流程
        dr.find_element_by_xpath("//table[@id='ctl00_cntGrid2_dgdData']/tbody/tr[2]/td[4]/a").click()
        #流程处理
        dr.find_element_by_id("ctl00_cntButton_FlowAction1_cmdFlMange").click()

        first_handle = dr.current_window_handle #获取当前窗口句柄
        print(first_handle)
        all_handles = dr.window_handles  # 获取所有窗口句柄        
        
        for handle in all_handles:
            if handle != first_handle:
                print(handle)                                           
                dr.switch_to.window(handle)
                dr.find_element_by_id("ctl00_cntForm_rdYes").click()
                dr.find_element_by_id("ctl00_cntButton_cmdOK").click()
                base.ExeMgr()
                sleep(3)
                # 下一步执行人
                base.choose_emp(dr,u"-流程申请人-")
                  
              
        dr.switch_to.window(first_handle)
        dr.switch_to.frame("indexFrame")
        dr.switch_to.frame("PageFrame")
        
        dr.find_element_by_id("ctl00_MsgTab1_lnk1").click()
        
        # 验证处理的发文
        dr.save_screenshot(self.cfg['test_output_path']+u"screenshot\处理收文.png")
        

####################################################################################################
    
    def tearDown(self):
        self.driver.quit()
        

if __name__ == "__main__":
    unittest.main()
