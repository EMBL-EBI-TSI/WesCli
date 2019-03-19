# encoding: utf-8

import unittest
from WesCli.Upload import upload


class UploadIntegrationTest(unittest.TestCase):
    
    def test_upload(self):
        '''
        wes upload https://tes.tsi.ebi.ac.uk/data/tmp/ file.txt
        '''
        
        upload('https://tes.tsi.ebi.ac.uk/data/tmp/', 'test/resources/Hello.txt')



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()