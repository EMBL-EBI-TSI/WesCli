import unittest
from WesCli.ArgParser import getOpts
from AssertKeyValueMixin import AssertKeyValueMixin


class ArgParserTest(unittest.TestCase, AssertKeyValueMixin):

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
        
        args = getOpts(['status'])
    
        print(args)
        
        '''
        {'<runSpec>': None,
         'run': False,
         'status': True}
        '''
        
        self.assertKeyValue(args, 'status', True)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()