# encoding: utf-8

import unittest
from WesCli.WesCli import run
from WesCli.either import Ok, Error


class IntegrationTest(unittest.TestCase):
    
    def test_run_success(self):
        
        r = run( 'http://localhost:8080/ga4gh/wes/v1'
               , 'https://github.com/fgypas/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'
               , '{ "input": {   "class": "File",   "location": "file:///tmp/hashSplitterInput/test.txt" } }'
               )
        
        print(r)   # Ok({'run_id': 'S28J1E'})
        
        self.assertEquals(type(r), Ok)
        self.assertTrue(len(r.v['run_id']) == 6)
        

    def test_run_failure(self):
        
        r = run( 'http://localhost:8080/ga4gh/wes/v1'
               , 'https://github.com/fgypas/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'
               , '{ "input": {   "class": "File",   "location": "file:///tmp/hashSplitterInput/test.txt"  }'  # <= removed one '}' :)
               )
        
        print(r)   # Error({'msg': 'The request is malformed.', 'status_code': '400'})
        
        self.assertEquals(type(r), Error)
        self.assertTrue('msg'           in r.v)
        self.assertTrue('status_code'   in r.v)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()