# encoding: utf-8

import unittest
from WesCli.WesCli import run, run_multiple, status, info, status_multiple
from WesCli.either import Ok, Error
from AssertKeyValueMixin import AssertKeyValueMixin
import os
from WesCli import LocalState
from WesCli.LocalState import DOT_FILE
from AssertThrowsMixin import AssertThrowsMixin
from WesCli.exception import UserMessageException



WES_URL = 'http://localhost:8080/ga4gh/wes/v1'
# WES_URL = 'https://tes.tsi.ebi.ac.uk/ga4gh/wes/v1'


class IntegrationTest(unittest.TestCase, AssertKeyValueMixin, AssertThrowsMixin):
    
        
    def setUp(self):
        
        self.maxDiff = None                 # Diff is 709 characters long. Set self.maxDiff to None to see it.
    

    def test_run_success(self):
        
        r = run( WES_URL
               , 'https://github.com/fgypas/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'
               , { "input": {   "class": "File",   "location": "file:///tmp/hashSplitterInput/test.txt" } }
               )
        
        print(r)   # Ok({'run_id': 'S28J1E'})
        
        self.assertEquals(type(r), Ok)
        self.assertTrue(len(r.v['run_id']) == 6)
        

    def test_run_failure(self):
        
        r = run( WES_URL
               , 'https://github.com/fgypas/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'
               , '{ "input": {   "class": "File",   "location": "file:///tmp/hashSplitterInput/test.txt"  }'  # <= removed one '}' :)
               )
        
        print(r)   # Error({'msg': 'The request is malformed.', 'status_code': '400'})
        
        self.assertEquals(type(r), Error)
        self.assertTrue('msg'           in r.v)
        self.assertTrue('status_code'   in r.v)

        
    def _test_run_failure_500(self):
        '''
        One day the cluster was not working and always returned this:
        
            500
    
            Body:
               <title>amqp.exceptions.NotFound: Queue.declare: (404) NOT_FOUND - home node 'rabbit@172.16.32.248' of durable queue 'celery' in vhost '/' is down or inaccessible // Werkzeug Debugger</title>
               (...) # Huge HTML

               
        -- and the client blew up.
        It was trying to convert the HTML to JSON.
        '''
        
        r = run( 'https://tes.tsi.ebi.ac.uk/ga4gh/wes/v1'
               , 'https://github.com/fgypas/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'
               , { "input": {   "class": "File",   "location": "file:///tmp/hashSplitterInput/test.txt" } }
               )
        
        print(r)   # Error({'status_code': 500, 'msg': 'INTERNAL SERVER ERROR'})
        
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

        
    def test_status_without_run(self):
        
        if os.path.exists(DOT_FILE): 
            os.remove(DOT_FILE)
        
        self.assertThrows( status_multiple
                         , UserMessageException
                         , "Local state file not found. Have you ran 'wes run' before?"
                         )
        
        
    def test_status_and_info(self):
        
        url = WES_URL
        
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