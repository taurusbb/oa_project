# coding=utf-8

import os,unittest,time
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
import yaml
import sys
sys.path.append("..")
import base

DEBUG = True

class add_fawen(unittest.TestCase):
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
    
    def test_add_fawen(self):
        dr = self.driver
        dr.get(self.base_url)
        #登录
        base.login(dr,self.cfg['username'],self.cfg['password'])

########################################新建发文####################################################
        name = u"发文" + '-' + time.strftime('%m%d-%H:%M:%S', time.localtime(time.time()))
        zihao = u"字号1"
        flowname = u"测试发文流程(重要)"
        sendgov = u"机关1"

        dr.switch_to.frame("indexFrame")
        dr.find_element_by_id("imgCloseRemind").click()
        dr.switch_to.frame("MenuFrame")
        # 新增发文
        # 点击公文管理节点
        dr.find_element_by_xpath("//div[@id='tree']/ul/li/ul/li[1]/ul/li[7]/span").click()        
        dr.find_element_by_xpath("//div[@id='tree']/ul/li/ul/li/ul/li[7]/ul/li[2]/a").click()

        dr.switch_to.default_content()
        dr.switch_to.frame("indexFrame")
        dr.switch_to.frame("PageFrame")

        dr.find_element_by_id("ctl00_cntGrid1_hypAdd").click()   

        # 填写标题
        dr.find_element_by_id("ctl00_cntForm_txtTitle").send_keys(name)
        dr.find_element_by_id("ctl00_cntForm_txtZihao").send_keys(zihao)
        Select(dr.find_element_by_id("ctl00_cntForm_FlowSelFlow1_drpFlow")).select_by_visible_text(flowname)
        Select(dr.find_element_by_id("ctl00_cntForm_drpDocNumberSet")).select_by_index(2)
        sleep(2)
        Select(dr.find_element_by_id("ctl00_cntForm_drpDocUnitWord")).select_by_index(2)
        sleep(2)
        dr.find_element_by_id("ctl00_cntForm_txtSendGov").send_keys(sendgov)



        first_handle = dr.current_window_handle #获取当前窗口句柄
        print(first_handle)

        # 新增发文稿纸
        dr.find_element_by_id("ctl00_cntForm_cmdDraft").click()
        sleep(10) #等待足够长的时间，直到稿纸模板窗口消失，剩下2个窗口，再执行下面脚本关闭文本编辑窗口。
        all_handles = dr.window_handles  # 获取所有窗口句柄        
        
        for handle2 in all_handles:
            if handle2 != first_handle:
                print(handle2)                                           
                dr.switch_to.window(handle2)                                          
                dr.close()                
                base.ExeMgr()
                break

        
        sleep(2)
        dr.switch_to_window(first_handle)
        dr.switch_to_frame("indexFrame")        
        dr.switch_to_frame("PageFrame")
        

        # 提交
        dr.find_element_by_id("ctl00_cntButton_FlowAction1_cmdSubmit").click()
        
        # 下一步执行人
        base.choose_emp(dr,u"-流程申请人-")



        # 验证新建发文
        dr.save_screenshot(self.cfg['test_output_path']+u"screenshot\新建发文.png")        

####################################################################################################




########################################流程处理####################################################

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
                sleep(2)
                # 下一步执行人
                base.choose_emp(dr,u"-流程申请人-")
                  
           
        dr.switch_to.window(first_handle)
        dr.switch_to.frame("indexFrame")        
        dr.switch_to.frame("PageFrame")
        dr.find_element_by_id("ctl00_MsgTab1_lnk1").click()
        # 验证处理的发文
        dr.save_screenshot(self.cfg['test_output_path']+u"screenshot\处理发文.png")
        

####################################################################################################


########################################套红步骤生成正式文件####################################################

        #待办流程
        dr.find_element_by_id("ctl00_MsgTab1_lnk0").click()
        #点击显示全部流程
        dr.find_element_by_id("ctl00_cntGrid2_TreeView1t0").click()
        #点击第一条流程
        dr.find_element_by_xpath("//table[@id='ctl00_cntGrid2_dgdData']/tbody/tr[2]/td[4]/a").click()

        first_handle = dr.current_window_handle #获取当前窗口句柄
        print(first_handle)
        #生成正式文件
        dr.find_element_by_id("ctl00_cntForm_cmdOfficial").click()
        sleep(10)
        all_handles = dr.window_handles  # 获取所有窗口句柄        
        
        for handle3 in all_handles:
            if handle3 != first_handle:
                print(handle3)                                           
                dr.switch_to.window(handle3)                                          
                dr.close()                
                base.ExeMgr()
                break                            
                
        sleep(3)
        
        dr.switch_to.window(first_handle)
        dr.switch_to.frame("indexFrame")        
        dr.switch_to.frame("PageFrame")

        #流程处理
        dr.find_element_by_id("ctl00_cntButton_FlowAction1_cmdFlMange").click()
        all_handles = dr.window_handles  # 获取所有窗口句柄        
        
        for handle in all_handles:
            if handle != first_handle:
                print(handle)                                           
                dr.switch_to.window(handle)
                dr.find_element_by_id("ctl00_cntForm_rdYes").click()
                dr.find_element_by_id("ctl00_cntButton_cmdOK").click()
                base.ExeMgr()                
                break
        sleep(3)
        dr.switch_to.window(first_handle)
        dr.switch_to.frame("indexFrame")        
        dr.switch_to.frame("PageFrame")
        dr.find_element_by_id("ctl00_MsgTab1_lnk3").click()
        #点击显示全部流程
        #dr.find_element_by_id("ctl00_cntGrid2_TreeView1t0").click()
        #点击第一条流程
        dr.find_element_by_xpath("//table[@id='ctl00_cntGrid2_dgdData']/tbody/tr[2]/td[3]/a").click()
        dr.save_screenshot(self.cfg['test_output_path']+u"screenshot\正式文件.png")
        

####################################################################################################

    
    def tearDown(self):
        self.driver.quit()
        

if __name__ == "__main__":
    unittest.main()
