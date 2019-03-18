# encoding: utf-8

import unittest
from WesCli.WesCli import run, run_multiple, status, info, status_multiple
from WesCli.either import Ok, Error
from AssertKeyValueMixin import AssertKeyValueMixin


class IntegrationTest(unittest.TestCase, AssertKeyValueMixin):
    
        
    def setUp(self):
        
        self.maxDiff = None                 # Diff is 709 characters long. Set self.maxDiff to None to see it.
    

    def test_run_success(self):
        
        r = run( 'http://localhost:8080/ga4gh/wes/v1'
               , 'https://github.com/fgypas/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'
               , { "input": {   "class": "File",   "location": "file:///tmp/hashSplitterInput/test.txt" } }
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
        

    def test_run_multiple(self):
        
        sites = run_multiple('examples/sitesWithError.yaml')
        
        self.assertGreater(len(sites), 1)


    def test_run_single(self):
        
        sites = run_multiple('examples/singleSite.yaml')
        
        self.assertTrue(len(sites) == 1)
        
        r = sites[0]
        
        self.assertKeyValue(r, 'url', 'http://localhost:8080/ga4gh/wes/v1')
        self.assertKeyValue(r, 'ok' , True)
        self.assertIsNotNone(r.get('id'))
            
            
    def test_status_multiple(self):
        
        print('-- run examples/sitesWithError.yaml ---------------------------------------')
        run_multiple('examples/sitesWithError.yaml')
        
        print()
        print('-- status_multiple() ------------------------------------------------------')
        status_multiple()
        

    def test_status_and_info(self):
        
        url = 'http://localhost:8080/ga4gh/wes/v1'
        
        r = run( url
               , 'https://github.com/fgypas/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'
               , { "input": {   "class": "File",   "location": "file:///tmp/hashSplitterInput/test.txt" } }
               )
        
        print(r)                                    # Ok({'run_id': 'S28J1E'})
        
        self.assertEquals(type(r), Ok)
        
        s = status(url, r.v['run_id'])
        
        print(s)                                    # Ok(UNKNOWN)
        
        self.assertEquals(type(s), Ok)
            
        i = info(url, r.v['run_id'])
        
        print(i)                                    # Ok({ 'outputs': {}, 'request': {'workflow_params': {'input': {'class': 'File', 'location': 'file:///tmp/hashSplitterInput/test.txt'}}, 
                                                    #      'workflow_type': 'cwl', 'workflow_type_version': 'v1.0', 
                                                    #      'workflow_url': 'https://github.com/fgypas/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'},
                                                    #      'run_log': {}, 'state': 'UNKNOWN', 'task_logs': [] })
        
        self.assertEquals(type(i), Ok)
            
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()