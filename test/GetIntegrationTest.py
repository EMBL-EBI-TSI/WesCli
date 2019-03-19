# encoding: utf-8

import unittest
from WesCli.Main import main


class GetIntegrationTest(unittest.TestCase):
    
    def test_get_dir(self):
        '''
        wes ls https://tes.tsi.ebi.ac.uk/data/tmp/
        '''
        
        main(['get', 'https://tes.tsi.ebi.ac.uk/data/tmp/'])
        
        
    def test_get_file(self):
        
        main(['get', 'https://tes.tsi.ebi.ac.uk/data/tmp/ZE4HDH/tmpo387m8k8/md5'])
        




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()