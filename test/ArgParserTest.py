import unittest
from WesCli.ArgParser import getOpts


class ArgParserTest(unittest.TestCase):

    def assertKeyValue(self, args, key, value):
        
        return self.assertEquals(args[key], value)


    def test_run(self):
        
        args = getOpts(['run', 'sites.yaml'])
    
        print(args)
        
        '''
         '<runSpec>': 'sites.yaml',
         'run': True,
        '''
        
        self.assertKeyValue(args, 'run'         , True)
        self.assertKeyValue(args, '<runSpec>'   , 'sites.yaml')
        

    def test_status(self):
        
        args = getOpts(['status', '6DNIPZ'])
    
        print(args)
        
        '''
         {'<runId>': '6DNIPZ',
          '<runSpec>': None,
          'run': False,
          'status': True}
        '''
        
        self.assertKeyValue(args, 'status'      , True)
        self.assertKeyValue(args, '<runId>'     , '6DNIPZ')
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()