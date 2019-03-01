# encoding: utf-8

import yaml
from jinja2 import Template
import requests
from WesCli.either import Ok, Error


def loadYaml(filename):
    
    with open(filename, 'r') as f:
        
        return yaml.safe_load(f)


def getEffectiveConf(conf):
    
    inputTemplate   = conf['inputTemplate']
    sites           = conf['sites']
    
    template = Template(inputTemplate)

    def renderSite(s):
        
        return {
            
            'url'   : s['url']
           ,'input' : template.render(s['inputTemplateParams'])
        }
        
    return {
        
        'workflow'  : conf['workflow']
       ,'sites'     : [ renderSite(s) for s in sites ]
    }


def run( wesUrl         : str
       , workflowUrl    : str
       , params         : str):
    
    '''
        curl -iv -X POST                                    \
             -H 'Content-Type: multipart/form-data'         \
             -H 'Accept: application/json'                  \
             -F workflow_params="$params"                   \
             -F workflow_type=cwl                           \
             -F workflow_type_version=v1.0                  \
             -F "workflow_url=$workflowUrl"                 \
             "$(wesUrl)/runs"
    '''
    
    r = requests.post(f"{wesUrl}/runs", data = {
        
          'workflow_type'           : 'cwl'         
         ,'workflow_type_version'   : 'v1.0'        
         ,'workflow_url'            : workflowUrl
         ,'workflow_params'         : params   
    })
    
    if   r.status_code == requests.codes.ok : return Ok(r.json())
    else                                    : return Error(r.json())


def run_multiple(yamlFilename):
    
    yaml = loadYaml(yamlFilename)
        
    conf = getEffectiveConf(yaml)
    
    workflow = conf['workflow']
    
    for s in conf['sites']:
        '''
        ,'sites': [
            { 'input' : '{ "input": {   "class": "File",   "location": "file:///tmp/hashSplitterInput/test1.txt" } }'
            , 'url'   : 'http://localhost:8080/ga4gh/wes/v1'
            }
        '''
        
        url   = s['url']
        input = s['input']
        
        print(f'{url}... ', end='')
        
        r = run(url, workflow, input)
        
        if   type(r) == Ok : print(r.v['run_id'])
        else               : print(r)

