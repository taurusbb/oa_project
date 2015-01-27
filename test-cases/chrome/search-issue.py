from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time
from selenium.webdriver.common.keys import Keys
import yaml
from pprint import pprint

DEBUG = True

class SearchIssue(unittest.TestCase):
    def loadInput(self, cfg):
        """load input data from search-issue.yaml"""
        try:
            stream = open(cfg['test_input_path']+'/search-issue.yaml', 'r')
        except Exception, e:
            print "cannot open " + cfg['test_input_path']+'/search-issue.yaml'
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
    
    def test_search_issue(self):
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

        for search in self.data['quick_search']:
            if DEBUG:
                print '-'*50;
                print 'Start quick search with ' + search[0]
                pprint(search)

            # start quick search
            driver.find_element_by_id("quickSearchInput").clear()
            driver.find_element_by_id("quickSearchInput").send_keys(search[0])
            driver.find_element_by_id("quickSearchInput").send_keys(Keys.RETURN)

            # check quick search result
            if DEBUG:
                print 'checking search result'

            for i in range(self.cfg['time_out']):
                try:
                    if self.is_element_present(By.ID, "key-val"): break
                except: pass
                time.sleep(1)
            else: self.fail("time out")

            time.sleep(2)
            try: self.assertEqual(search[1], driver.title)
            except AssertionError as e: self.verificationErrors.append(str(e))

            if DEBUG:
                print 'search result check...ok'
                print

        for advsearch in self.data['advanced_search']:
            time.sleep(2)
            if DEBUG:
                print '-'*50;
                print 'Start advanced search with ' + advsearch[0]
                pprint(advsearch)

            # start advanced search
            driver.find_element_by_id("advanced-search").clear()
            driver.find_element_by_id("advanced-search").send_keys(advsearch[0])
            driver.find_element_by_id("advanced-search").send_keys(Keys.RETURN)

            # check advanced search result
            if DEBUG:
                print 'checking search result'

            time.sleep(2)

            for i in range(self.cfg['time_out']):
                try:
                    if self.is_element_present(By.ID, "key-val"): break
                except: pass
                time.sleep(1)
            else: self.fail("time out")

            try: self.assertEqual(advsearch[1], driver.title)
            except AssertionError as e: self.verificationErrors.append(str(e))

            if DEBUG:
                print 'search result check...ok'
                print
    
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
