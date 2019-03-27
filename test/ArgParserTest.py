import unittest
from WesCli.ArgParser import getOpts, hasWatch
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


    def test_status_watch(self):
        
        args = getOpts(['status', '--watch'])
    
        print(args)
        
        '''
        {'--watch': True,
         '-w': False,
         'status': True}
        '''
        
        self.assertKeyValue(args, 'status' , True)
        self.assertTrue(hasWatch(args))
        
        self.assertTrue  ( hasWatch( getOpts(['status', '--watch'])   ))
        self.assertTrue  ( hasWatch( getOpts(['status', '-w'])        ))
        
        self.assertFalse ( hasWatch( getOpts(['status'])              ))


    def test_ls(self):
        
        args = getOpts(['get', 'https://tes.tsi.ebi.ac.uk/data/tmp/'])
    
        print(args)
        
        '''
        'get': True,
        '<url>': 'https://tes.tsi.ebi.ac.uk/data/tmp/',
        '''
        
        self.assertKeyValue(args, 'get'     , True)
        self.assertKeyValue(args, '<url>'   , 'https://tes.tsi.ebi.ac.uk/data/tmp/')
        

        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()