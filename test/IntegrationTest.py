# encoding: utf-8

import unittest
from WesCli.WesCli import run, Ok


class IntegrationTest(unittest.TestCase):
    
    def test_run(self):
        
        r = run( 'http://localhost:8080/ga4gh/wes/v1'
               , 'https://github.com/fgypas/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'
               , '{ "input": {   "class": "File",   "location": "file:///tmp/hashSplitterInput/test.txt" } }'
               )
        
        print(r)   # Ok({'run_id': 'S28J1E'})
        
        self.assertEquals(type(r), Ok)
        self.assertTrue(len(r.v['run_id']) == 6)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()