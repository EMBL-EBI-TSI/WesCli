# encoding: utf-8

import yaml
from jinja2 import Template
import requests
from WesCli.either import Ok, Error, Either
import json
from WesCli.LocalState import LocalState
from pydash.collections import partition
from WesCli.exception import InvalidConf


def loadYaml(filename):
    
    with open(filename, 'r') as f:
        
        return yaml.safe_load(f)


def hasTemplateParams(sites):

    has, hasnt = partition(sites, lambda s: 'inputParams' in s)
    
    if   len(has)   == len(sites) : return True
    elif len(hasnt) == len(sites) : return False
    else                          : raise InvalidConf()
    
    
def getEffectiveConf(conf):
    
    return replaceVariables(conf) if hasTemplateParams(conf['sites']) else conf
    
    
def replaceVariables(conf):
    
    inputTemplate   = conf['input']
    sites           = conf['sites']
    
    template = Template(inputTemplate)

    def renderSite(s):
        
        return {
            
            'url'   : s['url']
           ,'input' : template.render(s['inputParams'])
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


def status(wesUrl, id) -> Either:
    
    r = requests.get(f"{wesUrl}/runs/{id}/status")
    
    if   r.status_code == requests.codes.ok : return Ok(r.json()['state'])
    else                                    : return Error(r.text)


def info(wesUrl, id):
    
    r = requests.get(f"{wesUrl}/runs/{id}")
    
    if   r.status_code == requests.codes.ok : return Ok(r.json())
    else                                    : return Error(r.text)


def run_multiple(yamlFilename):
    
    yaml = loadYaml(yamlFilename)
        
    conf = getEffectiveConf(yaml)
    
    workflow = conf['workflow']
    
    localState = LocalState(workflow)
    
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
        
        print(r.v['run_id'] if r.isOk() else str(r))

        r.map(lambda v: v['run_id'])      # Ok({'run_id': 'S28J1E'}) => Ok('S28J1E')
        
        localState.add(url, r)  # , inputTemplateParams    # TODO?
        localState.save()


def formatOutputs(outputs):
    '''
    {
      "output": {
        "basename": "unify",
        "checksum": "sha1$e823b2bf8f0babdabe0e4c7399d8afe6ece73aec",
        "class": "File",
        "location": "file:///tmp/tmpjt14260x/unify",
        "path": "/tmp/tmpjt14260x/unify",
        "size": 413
      }
    }
    '''
    
    return { name: o['path'] for (name, o) in outputs.items() }


def status_multiple():
    
    s = LocalState('')
        
    s.load()
    
    '''
        'workflowUrl' : 'https://workflowhub.org/my-workflow.cwl'
       ,'sites': [
           
            { 'url' : 'http://localhost:8080/ga4gh/wes/v1', 'ok': True,  'id'    : '6DNIPZ' }
           ,{ 'url' : 'http://localhost:8081/ga4gh/wes/v1', 'ok': True,  'id'    : 'KSSGG3' }
           ,{ 'url' : 'http://localhost:8082/ga4gh/wes/v1', 'ok': False, 'error' : 'Something terrible happened.' }
        ]
    '''
    
    sites = s.sites
    
    successes, failures = partition(sites, lambda s: s['ok'])
    
    for site in successes:
        
        st = info(site['url'], site['id'])
        
        state   = st.v['state']                     if st.isOk() else ''
        outputs = formatOutputs(st.v['outputs'])    if st.isOk() else ''
        
        print(f"{site['url']}  {site['id']}  {state}  {outputs}")
        
    print()
    print('Failures:')
        
    for site in failures:
        
        print(f"{site['url']}  {site['error']}")
        
    
    



