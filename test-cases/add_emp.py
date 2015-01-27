# coding=utf-8

import os,unittest,time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import yaml
import sys
sys.path.append("..")
import base



DEBUG = True

class add_emp(unittest.TestCase):
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
        
    
    def test_add_emp(self):
        """Add emp checking """
        name = "test"+time.strftime('%m%d-%H%M%S',time.localtime(time.time()))

        
        dr = self.driver
        dr.get(self.base_url)
        
        #登录
        base.login(dr,self.cfg['admin'],self.cfg['password'])

        dr.switch_to.frame("indexFrame")
        dr.switch_to.frame("MenuFrame")
        #新增人员
        dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        dr.find_element_by_xpath("//div[@id='tree']/ul/li/ul/li[3]/a").click()
        dr.switch_to.default_content()
        dr.switch_to.frame("indexFrame")
        dr.switch_to.frame("PageFrame")
        dr.find_element_by_id("ctl00_cntGrid1_lnkAdd").click()
        #填写人员姓名
        dr.find_element_by_id("ctl00_cntForm_txtName").send_keys(name)
        #填写登陆账号
        dr.find_element_by_id("ctl00_cntForm_txtLoginid").send_keys(name)
        #填写部门职位
        Select(dr.find_element_by_id("ctl00_cntForm_EmpDepPos1_drpDep")).select_by_visible_text(u"人力资源部")
        #Select(dr.find_element_by_id("ctl00_cntForm_EmpDepPos1_drpPos")).select_by_value("9")
        #填写登陆密码
        dr.find_element_by_id("ctl00_cntForm_txtInitPW").send_keys("123456")
        dr.find_element_by_id("ctl00_cntForm_txtCheckPW").send_keys("123456")
        #保存退出
        dr.find_element_by_id("ctl00_cntButton_cmdSaveExi").click()


        #验证新增成功
        dr.find_element_by_id("ctl00_cntQuery_SeachSel1_IoFieldQuery1_txtSimple").send_keys(name)
        dr.find_element_by_id("ctl00_cntQuery_cmdQuery").click()

      
        # self.assertTrue(sel.is_element_present("xpath=//div[@id='ctl00_cntGrid2_updatePanel1']/table/tbody/tr[2]/td[2]/a"))        
        dr.find_element_by_xpath("//div[@id='ctl00_cntGrid2_updatePanel1']/table/tbody/tr[2]/td[2]/a").click()
        
        #验证姓名
        tname = dr.find_element_by_id("ctl00_cntForm_txtName").get_attribute("value")
        lname = dr.find_element_by_id("ctl00_cntForm_txtLoginid").get_attribute("value")        
        self.assertEqual(tname,name,"username incorrect")
        self.assertEqual(lname,name,"loginid incorrect") 
        

        dr.save_screenshot(self.cfg['test_output_path']+u"screenshot\新增人员.png")

    
    def tearDown(self):
        self.driver.quit()
        

if __name__ == "__main__":
    unittest.main()
