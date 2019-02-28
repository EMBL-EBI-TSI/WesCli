# encoding: utf-8

import unittest
from pprint import pprint
from WesCli.WesCli import loadYaml


class Test(unittest.TestCase):

    def test_loadYaml(self):
        
        yaml = loadYaml('examples/sites.yaml')
        
        pprint(yaml)
        
        
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()