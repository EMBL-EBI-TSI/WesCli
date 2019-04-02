# encoding: utf-8

import unittest
from WesCli.Upload import upload
from WesCli.Main import main
from urllib.parse import urljoin
from uuid import uuid4
from WesCli.Get import cat



def randomSubDir():
    
    return f'https://tes.tsi.ebi.ac.uk/data/tmp/subDirTest/{uuid4()}/'


class UploadIntegrationTest(unittest.TestCase):
    
    def test_upload(self):
        '''
        wes upload https://tes.tsi.ebi.ac.uk/data/tmp/ file.txt
        '''
        
        upload('https://tes.tsi.ebi.ac.uk/data/tmp/', 'test/resources/Hello.txt')
        
        self.assertEquals(cat('https://tes.tsi.ebi.ac.uk/data/tmp/Hello.txt'), 'Hello, world!')
        

    def test_upload_cmd_line(self):
        
        main(['upload', 'https://tes.tsi.ebi.ac.uk/data/tmp/', 'test/resources/Hello.txt'])


    def test_upload_to_subdir_with_different_filename(self):
        
        dirUrl = randomSubDir()
        fileUrl = urljoin(dirUrl, 'Hello2.txt')
        
        upload(fileUrl, 'test/resources/Hello.txt')
        
        self.assertEquals(cat(fileUrl), 'Hello, world!')
        
        
    def test_upload_to_subdir(self):
        
        dirUrl = randomSubDir()
        
        upload(dirUrl, 'test/resources/Hello.txt')
        
        fileUrl = urljoin(dirUrl, 'Hello.txt')
        
        self.assertEquals(cat(fileUrl), 'Hello, world!')


    def test_nice_error_message(self):
        
        main(['upload', 'https://tes.tsi.ebi.ac.uk/data/', 'test/resources/Hello.txt'])




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()