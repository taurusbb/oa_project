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

class CreateIssue(unittest.TestCase):
    def loadInput(self, cfg):
        """load input data from create-issue.yaml"""
        try:
            stream = open(cfg['test_input_path']+'/create-issue.yaml', 'r')
        except Exception, e:
            print "cannot open " + cfg['test_input_path']+'/create-issue.yaml'
            raise e
        data = yaml.load(stream)
        return data

    def setUp(self):
        self.cfg = testvars
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(self.cfg['implicit_wait'])
        self.base_url = self.cfg['base_url']
        self.verificationErrors = []
        self.accept_next_alert = True

        self.data = self.loadInput(self.cfg)
    
    def test_create_issue(self):
        driver = self.driver

        # open and wait for login page
        driver.get(self.base_url)
        driver.maximize_window()
        # for i in range(self.cfg['time_out']):
        #     try:
        #         if self.is_element_present(By.CSS_SELECTOR, "div.aui-pageheader-main > h1"): break
        #     except: pass
        #     time.sleep(1)
        # else: self.fail("time out")

        # login and wait for system dashboard page is loaded
        driver.find_element_by_id("login-form-username").clear()
        driver.find_element_by_id("login-form-username").send_keys(self.cfg['username'])
        driver.find_element_by_id("login-form-password").clear()
        driver.find_element_by_id("login-form-password").send_keys(self.cfg['password'])
        driver.find_element_by_id("login-form-submit").click()

        for fields in self.data['issue_fields']:
            issue_uniq_string = str(uuid.uuid4())
            issue_uniq_string = '_new_' + issue_uniq_string
            if DEBUG:
                print '-'*50;
                print 'Start creating issue with uniq string ' + issue_uniq_string
                pprint(fields)
                print

            # open and wait for dashboard page
            driver.get(self.base_url + "secure/Dashboard.jspa")

            # open and wait for create issue dialog is loaded
            driver.find_element_by_id("create_link").click()
            for i in range(self.cfg['time_out']):
                try:
                    if self.is_element_present(By.CSS_SELECTOR, "h2[title=\"Create Issue\"]"): break
                except: pass
                time.sleep(1)
            else: self.fail("time out")

            # fill issue fields
            # summary
            driver.find_element_by_id("summary").clear()
            driver.find_element_by_id("summary").send_keys(fields["summary"]+issue_uniq_string)

            # priority
            driver.find_element_by_xpath("//div[@id='priority-single-select']/span").click()
            driver.find_element_by_link_text(fields["priority"]).click()

            # due date
            driver.find_element_by_id("duedate").clear()
            driver.find_element_by_id("duedate").send_keys(fields["duedate"])

            # components
            for c in fields['components']:
                driver.find_element_by_xpath("//div[@id='components-multi-select']/span").click()
                driver.find_element_by_link_text(c).click()

            # affected versions
            for v in fields['affected_versions']:
                driver.find_element_by_xpath("//div[@id='versions-multi-select']/span").click()
                driver.find_element_by_link_text(v).click()

            # fixed versions
            for fv in fields['fix_versions']:
                driver.find_element_by_xpath("//div[@id='fixVersions-multi-select']/span").click()
                driver.find_element_by_link_text(fv).click()

            # assignee
            driver.find_element_by_id("assignee-field").click()
            driver.find_element_by_id("assignee-field").clear()
            driver.find_element_by_id("assignee-field").send_keys('')
            driver.find_element_by_id("assignee-field").clear()
            driver.find_element_by_id("assignee-field").send_keys(fields['assignee'])

            # click create button and wait till page load ready
            driver.find_element_by_id("create-issue-submit").click()
            for i in range(self.cfg['time_out']):
                try:
                    if self.is_element_present(By.CSS_SELECTOR, "div.aui-page-header-main > h1"): break
                except: pass
                time.sleep(1)
            else: self.fail("time out")

            if DEBUG:
                print 'issue created'
            
            time.sleep(3)
            
            # check issue details
            # quick search for the issue
            driver.get('http://localhost:8080/issues/?jql=summary ~ "'+issue_uniq_string+'"')
            for i in range(self.cfg['time_out']):
                try:
                    if self.is_element_present(By.XPATH, "//ul[@id='issuedetails']/li[7]/div/strong"): break
                except: pass
                time.sleep(1)
            else: self.fail("time out")

            # open issue page
            driver.find_element_by_id("key-val").click()

            # verify fields
            if DEBUG:
                print 'checking issue fields'

            # check summary
            try: self.assertEqual(fields["summary"]+issue_uniq_string, driver.find_element_by_id("summary-val").text)
            except AssertionError as e: self.verificationErrors.append(str(e))

            # check priority
            try: self.assertEqual(fields["priority"], driver.find_element_by_id("priority-val").text)
            except AssertionError as e: self.verificationErrors.append(str(e))

            # check versions affected
            try: self.assertEqual(', '.join(fields['affected_versions']), driver.find_element_by_id("versions-field").text)
            except AssertionError as e: self.verificationErrors.append(str(e))

            # check fix versions
            try: self.assertEqual(', '.join(fields['fix_versions']), driver.find_element_by_id("fixVersions-field").text)
            except AssertionError as e: self.verificationErrors.append(str(e))

            # check components
            try: self.assertEqual(', '.join(fields['components']), driver.find_element_by_id("components-field").text)
            except AssertionError as e: self.verificationErrors.append(str(e))

            if DEBUG:
                print 'issue fields checking... ok'
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
