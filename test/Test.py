# encoding: utf-8

import unittest
from pprint import pprint
from WesCli.WesCli import loadYaml, getEffectiveConf
from jinja2 import Template


class Test(unittest.TestCase):
    
    def setUp(self):
        
        self.maxDiff = None                 # Diff is 709 characters long. Set self.maxDiff to None to see it.
    

    def test_loadYaml(self):
        
        yaml = loadYaml('examples/sites.yaml')
        
        pprint(yaml)
        
    
    def test_renderTemplate(self):
        
        template = Template('Hello {{ name }}!')
        txt = template.render(name='world')
        
        self.assertEquals(txt, 'Hello world!')


    def test_getEffectiveConf(self):
            '''
            {'inputTemplate': '{ "input": {   "class": "File",   "location": "{{input}}" } '
                              '}',
                              
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
                            { 'input' : '{ "input": {   "class": "File",   "location": "file:///tmp/hashSplitterInput/test1.txt" } }'
                            , 'url'   : 'http://localhost:8080/ga4gh/wes/v1'
                            }
                          , { 'input' : '{ "input": {   "class": "File",   "location": "file:///tmp/hashSplitterInput/test2.txt" } }'
                            , 'url'   : 'http://localhost:8080/ga4gh/wes/v1'
                            }
                          ]
            })
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()