from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import unittest, time, re
import yaml
import uuid
from pprint import pprint

DEBUG = True

class UpdateIssue(unittest.TestCase):
    def loadInput(self, cfg):
        """load input data from update-issue.yaml"""
        try:
            stream = open(cfg['test_input_path']+'/update-issue.yaml', 'r')
        except Exception, e:
            print "cannot open " + cfg['test_input_path']+'/update-issue.yaml'
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
    
    def test_update_issue(self):
        driver = self.driver

        # open and wait for login page
        driver.get(self.base_url + "/login")
        driver.maximize_window()
        for i in range(self.cfg['time_out']):
            try:
                if self.is_element_present(By.CSS_SELECTOR, "div.aui-pageheader-main > h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")

        # login and wait for system dashboard page is loaded
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(self.cfg['username'])
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(self.cfg['password'])
        driver.find_element_by_id("login").click()

        for fields in self.data['issue_fields']:
            issue_uniq_string = str(uuid.uuid4())
            issue_uniq_string = '_updated_' + issue_uniq_string

            if DEBUG:
                print '-'*50;
                print 'Start updating issue with uniq string ' + issue_uniq_string
                pprint(fields)
                print

            # search for an open issue

            driver.get('https://ralphwen.atlassian.net/issues/?jql=summary ~ \"new_*\" and status = Open')
            for i in range(self.cfg['time_out']):
                try:
                    if self.is_element_present(By.XPATH, "//ul[@id='issuedetails']/li[7]/div/strong"): break
                except: pass
                time.sleep(1)
            else: self.fail("time out")

            for i in range(self.cfg['time_out']):
                try:
                    if self.is_element_present(By.ID, "key-val"): break
                except: pass
                time.sleep(1)
            else: self.fail("time out")

            # open issue page
            driver.find_element_by_id("key-val").click()
            for i in range(self.cfg['time_out']):
                try:
                    if self.is_element_present(By.ID, "summary-val"): break
                except: pass
                time.sleep(1)
            else: self.fail("time out")

            # click edit button
            driver.find_element_by_css_selector("span.trigger-label").click()
            for i in range(self.cfg['time_out']):
                try:
                    if self.is_element_present(By.CSS_SELECTOR, "div.content > div.field-group > label"): break
                except: pass
                time.sleep(1)
            else: self.fail("time out")

            # update issue
            # summary
            driver.find_element_by_id("summary").clear()
            driver.find_element_by_id("summary").send_keys(fields["summary"]+issue_uniq_string)

            # due date
            driver.find_element_by_id("duedate").clear()
            driver.find_element_by_id("duedate").send_keys(fields["duedate"])

            # environment
            driver.find_element_by_id("environment").clear()
            driver.find_element_by_id("environment").send_keys(fields["environment"])

            # environment preview
            if fields["env_preview"] == "True":
                driver.find_element_by_css_selector("#environment-preview_link > span.aui-icon.wiki-renderer-icon").click()

            time.sleep(3)

            # click update
            driver.find_element_by_id("edit-issue-submit").click()
            for i in range(self.cfg['time_out']):
                try:
                    if self.is_element_present(By.ID, "key-val"): break
                except: pass
                time.sleep(1)
            else: self.fail("time out")

            time.sleep(3)

            if DEBUG:
                print 'issue updated'

            # check issue fields
            if DEBUG:
                print 'checking issue fields'
            
            # check summary
            try: self.assertEqual(fields["summary"]+issue_uniq_string, driver.find_element_by_id("summary-val").text)
            except AssertionError as e: self.verificationErrors.append(str(e))

            # check due date
            try: self.assertEqual(fields["duedate"], driver.find_element_by_css_selector("time").text)
            except AssertionError as e: self.verificationErrors.append(str(e))

            if DEBUG:
                print 'issue fields checking... ok'
                print
            time.sleep(3)
    
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
