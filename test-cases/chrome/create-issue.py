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
import base

DEBUG = True

class CreateIssue(unittest.TestCase):
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
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(self.cfg['implicit_wait'])
        self.base_url = self.cfg['base_url']
        self.verificationErrors = []
        self.accept_next_alert = True

        self.data = self.loadInput(self.cfg)
    
    def test_create_issue(self):
        driver = self.driver

        # open and wait for login page
        driver.get(self.base_url)


        if DEBUG:
            print u'传阅 checking... ok'
            print
        time.sleep(2)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
