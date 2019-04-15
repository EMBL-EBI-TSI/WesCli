# encoding: utf-8

import unittest
from WesCli.Get import newFormatLine


class GetTest(unittest.TestCase):
    
    def setUp(self):
        
        self.maxDiff = None                 # Diff is 709 characters long. Set self.maxDiff to None to see it.
    

    def test_formatLine(self):
        '''
        ZE4HDH/                        (file://data/tmp//ZE4HDH/)
        Hello.txt                      (file://data/tmp//Hello.txt)
        '''
        
        helloFile = {
            
            'IsDir': False,
            'IsSymlink': False,
            'ModTime': '2019-03-26T16:32:52.573193293Z',
            'Mode': 384,
            'Name': 'Hello.txt',
            'Size': 13,
            'URL': './Hello.txt'
        }
        
        aDir = {
            
            'IsDir': True,
            'IsSymlink': False,
            'ModTime': '2019-03-14T14:19:40.6140346Z',
            'Mode': 2151678445,
            'Name': 'ZE4HDH',
            'Size': 4096,
            'URL': './ZE4HDH/'
        }
        
        
        formatLine = newFormatLine('https://tes.tsi.ebi.ac.uk/data/tmp/')
        
        self.assertEquals(formatLine(helloFile) , 'Hello.txt                      (file:///data/tmp/Hello.txt)' )
        self.assertEquals(formatLine(aDir)      , 'ZE4HDH/                        (file:///data/tmp/ZE4HDH/)'   )
        
        
    
    





if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()