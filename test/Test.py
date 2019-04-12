# encoding: utf-8

import unittest
from pprint import pprint
from WesCli.WesCli import loadYaml, getEffectiveConf, validateSites, replace,\
    statusLine, info
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
        
        line = statusLine(url, id, Ok({
            
            'outputs': {'output': {'basename': 'unify',
                        'checksum': 'sha1$4933476da50795db219640556d5cc613ca3804e1',
                        'class': 'File',
                        'location': 'file:///data/tmp/7GOLQ0/tmphay73miu/unify',
                        'path': '/data/tmp/7GOLQ0/tmphay73miu/unify',
                        'size': 413}}

           ,'state': 'COMPLETE'
        }))
            
        self.assertEquals(line.split('\n'), [
            
            'https://tes.tsi.ebi.ac.uk/ga4gh/wes/v1  7GOLQ0  COMPLETE'
           ,'Outputs:'
           ,'output: https://tes.tsi.ebi.ac.uk/data/tmp/7GOLQ0/tmphay73miu/unify'
           ,''
        ])
            

    def test_statusLine_Maxim_outputs(self):

        url = 'http://localhost:8080/ga4gh/wes/v1'
        id  = 'J6WLTA'
        
        #########################################################################################################
        
#         st = info(url, id)
#         
#         pprint(st.v)   # DEBUG
#         
#         s = statusLine(url, id, st)
#         
#         print(s)
        
        #########################################################################################################
        
        line = statusLine(url, id, Ok({
                 
                'outputs': {
                    
#                     'cmsearch_matches': [{'basename': 'mrum-genome.fa.cmsearch_matches.tbl',
#                                    'checksum': 'sha1$2bb3f921e9d2bfd590c4ca9a0a7d6ce24b4bf07a',
#                                    'class': 'File',
#                                    'location': 'file:///tmp/tmp7g11r1hn/mrum-genome.fa.cmsearch_matches.tbl',
#                                    'path': '/tmp/tmp7g11r1hn/mrum-genome.fa.cmsearch_matches.tbl',
#                                    'size': 8236},
#                                   {'basename': 'mrum-genome.fa.cmsearch_matches.tbl',
#                                    'checksum': 'sha1$6f2024e21ca2a16a8f04f03eb64fe3a19e930f7c',
#                                    'class': 'File',
#                                    'location': 'file:///tmp/tmp9cplgp_f/mrum-genome.fa.cmsearch_matches.tbl',
#                                    'path': '/tmp/tmp9cplgp_f/mrum-genome.fa.cmsearch_matches.tbl',
#                                    'size': 1176}],
                    
                    'concatenate_matches': {'basename': 'cat_cmsearch_matches.tbl',
                                     'checksum': 'sha1$158894850248d5d9510b235b5c02dc106da26532',
                                     'class': 'File',
                                     'location': 'file:///tmp/tmprl5mn1th/cat_cmsearch_matches.tbl',
                                     'path': '/tmp/tmprl5mn1th/cat_cmsearch_matches.tbl',
                                     'size': 9412},
                    
                    'deoverlapped_matches': {'basename': 'cat_cmsearch_matches.tbl.deoverlapped',
                                      'checksum': 'sha1$4d88865ee67b33fbf3db268a211fce9dbff715dd',
                                      'class': 'File',
                                      'location': 'file:///tmp/tmpeygi49er/cat_cmsearch_matches.tbl.deoverlapped',
                                      'path': '/tmp/tmpeygi49er/cat_cmsearch_matches.tbl.deoverlapped',
                                      'size': 7490}}
     
               ,'state': 'COMPLETE'
            }))
        
        print(line)
            
        self.assertEquals(line.split('\n'), [
                
            'http://localhost:8080/ga4gh/wes/v1  J6WLTA  COMPLETE'
           ,'Outputs:'
           ,'concatenate_matches: http://localhost:8080/tmp/tmprl5mn1th/cat_cmsearch_matches.tbl'
           ,'deoverlapped_matches: http://localhost:8080/tmp/tmpeygi49er/cat_cmsearch_matches.tbl.deoverlapped'
           ,''
        ])


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