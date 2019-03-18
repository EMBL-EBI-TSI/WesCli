# encoding: utf-8

import unittest
from WesCli import Ls


class LsIntegrationTest(unittest.TestCase):
    
    def test_ls(self):
        '''
        wes ls https://tes.tsi.ebi.ac.uk/data/tmp/
        '''
        
        Ls.cmd('https://tes.tsi.ebi.ac.uk/data/tmp/')
        
        
        






if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()