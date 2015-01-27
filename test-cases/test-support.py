# coding=utf-8

import os,unittest
from selenium import webdriver


import sys
sys.path.append("..")
import base

# from selenium.webdriver.support import expected_conditions as EC


DEBUG = True

class support(unittest.TestCase):


    def setUp(self):

        iedriver = "D:\python27\IEDriverServer.exe"
        os.environ["webdriver.ie.driver"] = iedriver
        self.driver = webdriver.Ie(iedriver)

        
    
    def test_support(self):
        """Check creating emp"""

        
        dr = self.driver
        dr.get("http://localhost:8007/ioffice")
        
        #登录
        base.login(dr,"admin","123456")

        dr.switch_to.frame("indexFrame")
        dr.switch_to.frame("MenuFrame")
        #新增人员
        dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        dr.find_element_by_xpath("//div[@id='tree']/ul/li/ul/li[3]/a").click()
        dr.switch_to.default_content()
        dr.switch_to.frame("indexFrame")
        dr.switch_to.frame("PageFrame")



        #验证新增成功
        dr.find_element_by_id("ctl00_cntQuery_SeachSel1_IoFieldQuery1_txtSimple").send_keys("may")
        dr.find_element_by_id("ctl00_cntQuery_cmdQuery").click()
            
       
        # self.assertTrue(EC.presence_of_element_located("//div[@id='ctl00_cntGrid2_updatePanel1']/table/tbody/tr[2]/td[2]/a"))        
        dr.find_element_by_xpath("//div[@id='ctl00_cntGrid2_updatePanel1']/table/tbody/tr[2]/td[2]/a").click()
        
        #验证姓名
        tname = dr.find_element_by_id("ctl00_cntForm_txtName").get_attribute("value")
        lname = dr.find_element_by_id("ctl00_cntForm_txtLoginid").get_attribute("value")        
        self.assertEqual(tname,"may1","username incorrect")
        self.assertEqual(lname,"may","loginid incorrect")           

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
