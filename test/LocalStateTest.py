# encoding: utf-8

import unittest
from WesCli.LocalState import LocalState


class LocalStateTest(unittest.TestCase):
    
    def setUp(self):
        
        self.maxDiff = None                 # Diff is 709 characters long. Set self.maxDiff to None to see it.
    

    def test_add(self):
        
        s = LocalState('https://workflowhub.org/my-workflow.cwl')
        
        s.add('http://localhost:8080/ga4gh/wes/v1', '6DNIPZ')
        s.add('http://localhost:8081/ga4gh/wes/v1', 'KSSGG3')
        s.add('http://localhost:8082/ga4gh/wes/v1', 'Something terrible happened.')
        
        print(s)
        
        self.assertEquals(s.asDict(), {
            
            'workflowUrl' : 'https://workflowhub.org/my-workflow.cwl'
           ,'sites': [
               
                { 'url' : 'http://localhost:8080/ga4gh/wes/v1', 'idOrError' : '6DNIPZ' }
               ,{ 'url' : 'http://localhost:8081/ga4gh/wes/v1', 'idOrError' : 'KSSGG3' }
               ,{ 'url' : 'http://localhost:8082/ga4gh/wes/v1', 'idOrError' : 'Something terrible happened.' }
            ]
        })
    
    
    def test_load_save(self):
    
        s1 = LocalState('')
        
        s2 = LocalState('https://workflowhub.org/my-workflow.cwl')
        s2.add('http://localhost:8080/ga4gh/wes/v1', '6DNIPZ')
        s2.add('http://localhost:8081/ga4gh/wes/v1', 'KSSGG3')
        s2.add('http://localhost:8082/ga4gh/wes/v1', 'Something terrible happened.')
        

        self.assertEquals(s1.asDict(), {'workflowUrl': '', 'sites': []})
        self.assertNotEquals(s1.asDict(), s2.asDict())
        
        s2.save()
        
        s1.load()
        
        self.assertEquals(s1.asDict(), s2.asDict())

        
        

            
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()