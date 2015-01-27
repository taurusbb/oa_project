# coding=utf-8

import os,unittest,time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import yaml
from time import sleep
import sys
sys.path.append("..")
import base

DEBUG = True

class add_chuanyue(unittest.TestCase):
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
    
    def test_add_chuanyue(self):
        """Chuanyue checking"""        
        name = u'传阅'+time.strftime('%m%d-%H:%M:%S',time.localtime(time.time()))

        dr = self.driver
        dr.get(self.base_url)
        #登录
        base.login(dr,self.cfg['username'],self.cfg['password'])
        dr.switch_to.frame("indexFrame")
        dr.find_element_by_id("imgCloseRemind").click()        
        dr.switch_to.frame("MenuFrame")
        #新增传阅
        dr.find_element_by_xpath("//div[@id='tree']/ul/li/ul/li/ul/li/ul/li[4]/a").click()
        
        dr.switch_to.default_content()
        dr.switch_to.frame("indexFrame")
        dr.switch_to.frame("PageFrame")

        dr.find_element_by_id("ctl00_cntGrid1_hlkAdd").click()
        #填写标题
        dr.find_element_by_id("ctl00_cntForm_txtSubject").send_keys(name)

        
        #添加传阅对象
        dr.find_element_by_id("ctl00_cntForm_cmdAdd").click() 
        sleep(3)
        Select(dr.find_element_by_id("ctl00_cntForm_lstEmp")).select_by_index(0)
        dr.find_element_by_id("ctl00_cntForm_cmdAdd").click()
        Select(dr.find_element_by_id("ctl00_cntForm_lstEmp")).select_by_index(1)
        dr.find_element_by_id("ctl00_cntForm_cmdAdd").click()
        dr.find_element_by_id("ctl00_cntButton_cmdOK").click()

        #上传附件
        dr.find_element_by_id("ctl00_cntForm_IoFileAtt1_File1").send_keys(u'F:\加班.txt')
        dr.find_element_by_id("ctl00_cntForm_IoFileAtt1_cmdUpFile").click()



        #填写正文
        dr.switch_to_frame("ctl00_cntForm_HtmlEditor1_FCKeditor1___Frame")
        dr.find_element_by_id("xEditingArea").send_keys(u"测试传阅啊！")


        dr.switch_to.default_content()
        dr.switch_to.frame("indexFrame")
        dr.switch_to.frame("PageFrame")

   

        #开始传阅
        dr.find_element_by_id("ctl00_cntButton_cmdStartMsg").click()


        #验证传阅
        dr.find_element_by_id("ctl00_MsgTab1_lnk2").click()
        dr.find_element_by_xpath("//table[@id='ctl00_cntGrid1_dgdData']/tbody/tr[2]/td[3]/a").click()
        dr.save_screenshot(self.cfg['test_output_path']+u"screenshot\传阅.png")
    
    def tearDown(self):
        self.driver.quit() 
        

if __name__ == "__main__":
    unittest.main()
