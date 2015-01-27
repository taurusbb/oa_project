OA-test
=========

This is a demo function test suite using selenium webdriver. 
The test suite is written in Python using unittest. It covers three 
major use cases: 

* issue creation
* issue searching
* issue updating

The test boasts the following features:

* data-driven
* cross-platform
* multi-browser support
* loosely coupled
* easy to extend
* easy to maintain


## Usage

To run the test, use `python run-test-suite.py [-h] [-c CONFIGFILE]`

You may use the -c switch to specify the test configuration file you
want to run against. The default file is `firefox-test-config.yaml`.

You may add new test cases to `YAML` files under the `test-input` folder.
Be careful when modifying them and please follow the `YAML` syntax.

Detailed test execution result will be echoed to console. Highlevel
test result will be generated under the `test-output` folder.

There is a module called `gen-input-from-raw.py` which is provided to generate
test config `YAML` files from 'raw' YAML files. However, it's not well tested yet.
