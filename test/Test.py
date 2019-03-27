# encoding: utf-8

import unittest
from pprint import pprint
from WesCli.WesCli import loadYaml, getEffectiveConf, validateSites, replace,\
    statusLine
from WesCli.exception import InvalidConf
from WesCli.either import Ok


class Test(unittest.TestCase):
    
    def setUp(self):
        
        self.maxDiff = None                 # Diff is 709 characters long. Set self.maxDiff to None to see it.
    

    def test_loadYaml(self):
        
        yaml = loadYaml('examples/sites.yaml')
        
        pprint(yaml)
        
    
    def test_replace(self):
        
        inputTree = { 
            
            "input": {
                
                "class"     : "File"
               ,"location"  : '$input'
        }}
        
        params = {'input': 'someValue'}
        
        self.assertEquals(replace(inputTree, params), { 
            
            "input": {
                
                "class"     : "File"
               ,"location"  : 'someValue'
        }})


    def test_getEffectiveConf(self):
            '''
            {'inputTemplate': { "input": {   "class": "File",   "location": "$input" } },
                              
             'sites': [{'inputTemplateParams': {'input': 'file:///tmp/hashSplitterInput/test1.txt'},
                        'site': 'http://localhost:8080/ga4gh/wes/v1'},
                       {'inputTemplateParams': {'input': 'file:///tmp/hashSplitterInput/test2.txt'},
                        'site': 'http://localhost:8080/ga4gh/wes/v1'}],
                        
             'workflow': 'https://github.com/fgypas/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'}
            '''
        
            yaml = loadYaml('examples/sites.yaml')
            
            self.assertEqual(getEffectiveConf(yaml), {
                
                 'workflow': 'https://github.com/fgypas/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'
                
                ,'sites': [
                            { 'input' : { "input": {   "class": "File",   "location": "file:///tmp/hashSplitterInput/test1.txt" } }
                            , 'url'   : 'http://localhost:8080/ga4gh/wes/v1'
                            }
                          , { 'input' : { "input": {   "class": "File",   "location": "file:///tmp/hashSplitterInput/test2.txt" } }
                            , 'url'   : 'http://localhost:8080/ga4gh/wes/v1'
                            }
                          ]
            })
        
        
    def test_getEffectiveConf_single_site(self):
        
        yaml = loadYaml('examples/singleSite.yaml')
        
        self.assertEqual(getEffectiveConf(yaml), {
                
             'workflow': 'https://github.com/fgypas/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'
            
            ,'sites': [
                
                { 'input' : { "input": {   "class": "File",   "location": "file:///tmp/hashSplitterInput/test1.txt" } }
                , 'url'   : 'http://localhost:8080/ga4gh/wes/v1'
                }
            ]
        })
            
            
    def test_hasTemplateParams(self):
        
        # Everybody has
        validateSites([
             
            { 'url': 'http://localhost:8080/ga4gh/wes/v1'
            , 'inputParams': { 'a': 1 }
            }
            
           ,{ 'url': 'http://localhost:8080/ga4gh/wes/v1'
            , 'inputParams': { 'a': 2 }
            }
        ])
        
        # Nobody has
        validateSites([
             
            {'url': 'http://localhost:8080/ga4gh/wes/v1'}
           ,{'url': 'http://localhost:8080/ga4gh/wes/v1'}
        ])

        # Somebody has => error
        with self.assertRaises(InvalidConf) as cm:
             
            validateSites([
             
                {'url': 'http://localhost:8080/ga4gh/wes/v1'}
                 
               ,{ 'url': 'http://localhost:8080/ga4gh/wes/v1'
                , 'inputParams': { 'a': 1 }
                }
            ])
            
        print(cm.exception)
        
    def test_statusLine(self):
        '''
        {
            'outputs': {'output': {'basename': 'unify',
                        'checksum': 'sha1$4933476da50795db219640556d5cc613ca3804e1',
                        'class': 'File',
                        'location': 'file:///data/tmp/7GOLQ0/tmphay73miu/unify',
                        'path': '/data/tmp/7GOLQ0/tmphay73miu/unify',
                        'size': 413}}

           ,'state': 'COMPLETE'
        }

        => https://tes.tsi.ebi.ac.uk/ga4gh/wes/v1  7GOLQ0  COMPLETE  {'output': '/data/tmp/7GOLQ0/tmphay73miu/unify'}
        '''

        url = 'https://tes.tsi.ebi.ac.uk/ga4gh/wes/v1'
        id  = '7GOLQ0'
        
        self.assertEquals(
                    
            statusLine(url, id, Ok({
                
                'outputs': {'output': {'basename': 'unify',
                            'checksum': 'sha1$4933476da50795db219640556d5cc613ca3804e1',
                            'class': 'File',
                            'location': 'file:///data/tmp/7GOLQ0/tmphay73miu/unify',
                            'path': '/data/tmp/7GOLQ0/tmphay73miu/unify',
                            'size': 413}}
    
               ,'state': 'COMPLETE'
            }))
            
            , "https://tes.tsi.ebi.ac.uk/ga4gh/wes/v1  7GOLQ0  COMPLETE  {'output': 'https://tes.tsi.ebi.ac.uk/data/tmp/7GOLQ0/tmphay73miu/unify'}"
        )


    def test_statusLine_no_outputs(self):
        '''
        {
           'outputs': {}
          ,'state': 'RUNNING'
        }
        '''

        url = 'https://tes.tsi.ebi.ac.uk/ga4gh/wes/v1'
        id  = '7GOLQ0'
        
        self.assertEquals(
                    
            statusLine(url, id, Ok({
                
                'outputs'   : {}
               ,'state'     : 'RUNNING'
            }))
            
            , "https://tes.tsi.ebi.ac.uk/ga4gh/wes/v1  7GOLQ0  RUNNING"
        )





if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()