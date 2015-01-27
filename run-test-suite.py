#!/usr/bin/env python

import os
import sys
import time
import yaml
import argparse
import unittest
from pprint import pprint
import HTMLTestRunner

DEBUG = True


class Tests():

    """used to put all test cases into a test suite"""

    def __init__(self, cfg):
        self.config = cfg

    def test_suite(self):
        """add all test cases listed in the test configuration
        file to a unittest test suite and return the test suite.
        test cases should exist in the TestCases folder with
        same names as listed in test configuration file provided."""

        alltests = unittest.TestSuite()

        sys.path.append(self.config['test_cases_path'])

        ms = []
        for fn in os.listdir(self.config['test_cases_path']):
            if fn.endswith('.py'):
                ms.append(fn[0:(len(fn) - 3)])

        for module in map(__import__, ms):
            # pass test configuration file to test casees
            module.testvars = self.config

            alltests.addTest(unittest.findTestCases(module))

        return alltests


if __name__ == "__main__":
    # command-line args processing
    parser = argparse.ArgumentParser(description="""
		This is a practice test automation project for JIRA.
		The test suite covers three major use cases for issue
		creation, update and search.""")

    parser.add_argument('-c', '--configfile', help="""
		provide your YAML file for test configuration here.
        The defalt file is firefox-test-config.yaml which can
        server as an example.""",
                        required=False)

    args = vars(parser.parse_args())

    # get the test configuration yaml file name from cmd line arg
    config_yaml = ""
    if not args["configfile"]:
        config_yaml = "ie-test-config.yaml"
    else:
        config_yaml = args["configfile"]

    try:
        try:
            # load the test configfile to a dict
            stream = open(config_yaml)
            config = yaml.load(stream)
        except IOError as ioe:
            print "Cannot open " + config_yaml

        if DEBUG:
            print '=' * 50
            print 'Test configuration'
            pprint(config)
            print

        # create test suite
        MyTests = Tests(config)

        # create test log file
        t = time.localtime()
        # ts = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + \
        # 	'_' + str(t.tm_hour) + '-' + str(t.tm_min) + '-' + str(t.tm_sec)
        # log = config['test_output_path'] + 'test_result-' + ts + '.log'
        # f = open(log, "a")
        ts = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + \
            '_' + str(t.tm_hour) + '-' + str(t.tm_min) + '-' + str(t.tm_sec)
        report = config['test_output_path'] + 'report-' + ts + '.html'

        with open(report, "w") as f:
            HTMLTestRunner.HTMLTestRunner(
            stream=f,
            title='Kaifaban19 report',
            verbosity=2,
            description='Sample test for HTMLTestRunner usage'
            ).run(MyTests.test_suite())

        # create command-line test runner
        # runner = unittest.TextTestRunner(f)
        # runner.verbosity = 2
        # start test execution
        # unittest.main(defaultTest='MyTests.test_suite', testRunner=runner)

            if DEBUG:
                print '#' * 50
                print 'Test finished. Please check log under ./' + config['test_output_path']

    except KeyError as ke:
        print "The test configuration file you provided is broken."
        if DEBUG:
            raise ke
