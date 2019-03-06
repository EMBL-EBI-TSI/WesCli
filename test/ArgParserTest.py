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
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()