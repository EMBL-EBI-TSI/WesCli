# encoding: utf-8

import yaml
import requests
from WesCli.either import Ok, Error, Either
from WesCli.LocalState import LocalState
from pydash.collections import partition
from WesCli.exception import InvalidConf
from pydash.predicates import is_string
from pydash.objects import map_values_deep, clone_deep
from typing import Optional, Union, List, Dict
import json
from pprint import pprint
from urllib.parse import urlsplit, urljoin
import os
from WesCli import url
from WesCli.url import getBaseUrl


def loadYaml(filename):
    
    with open(filename, 'r') as f:
        
        return yaml.safe_load(f)


def validateSites(sites):

    has, hasnt = partition(sites, lambda s: 'inputParams' in s)
    
    ok = len(has)   == len(sites) or \
         len(hasnt) == len(sites)
    
    if not ok: raise InvalidConf("Invalid configuration. Either all sites have 'inputParams' or none should have.")
    
    
def getEffectiveConf(conf):
    
    validateSites(conf['sites'])
    
    return replaceVariables(conf)
    
    
def mapTree(tree, func):
    '''
    map_values_deep() mutates the tree.
    
    So, I clone it first.
    '''
    
    return map_values_deep(clone_deep(tree), func)


def replace(inputTree, params):
    
    def isVariable(x):        return is_string(x) and len(x) != 0 and x[0] == '$'
    
    def variableValue(name):  return params[name[1:]]  # The 1st char is '$'

    def func(x):
          
        if isVariable(x):
            return variableValue(x)
        else:       
            return x
        
     
    return mapTree(inputTree, func)


def replaceVariables(conf):
    
    inputTree   = conf['input']
    sites       = conf['sites']

    def renderSite(s):
        
        inputParams = s.get('inputParams')
        
        return {
            
            'url'   : s['url']
           ,'input' : replace(inputTree, inputParams) if inputParams else inputTree
        }
        
    return {
        
        'workflow'  : conf['workflow']
       ,'sites'     : [ renderSite(s) for s in sites ]
    }


def toJson(r):
    
    try:
        
        return r.json()
    
    except:
        
        return {
            
            'status_code'   : r.status_code
           ,'msg'           : r.reason
        }
    

def run( wesUrl         : str
       , workflowUrl    : str
       , params         : dict):
    
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
         ,'workflow_params'         : json.dumps(params)   
    })
    
    if   r.status_code == requests.codes.ok : return Ok(r.json())              # @UndefinedVariable
    else                                    : return Error(toJson(r))


def status(wesUrl, id) -> Either:
    
    r = requests.get(f"{wesUrl}/runs/{id}/status")
    
    if   r.status_code == requests.codes.ok : return Ok(r.json()['state'])     # @UndefinedVariable
    else                                    : return Error(r.text)


def info(wesUrl, id):
    
    r = requests.get(f"{wesUrl}/runs/{id}")
    
    if   r.status_code == requests.codes.ok : return Ok(r.json())              # @UndefinedVariable
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
    
        
    return localState.sites


def pickUrls(outputsBaseUrl, outputs):
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
    
    def outputUrl(o: Union[List, Dict]):
        
        def f(o : Dict):
            try:
                return urljoin(outputsBaseUrl, o['path'])
            except:
                return None

        
        if isinstance(o, List) : return [f(x) for x in o]
        else                   : return f(o)


    return { name: outputUrl(o) for (name, o) in outputs.items() }


def formatOutputs(outputs):
    
    return 'Outputs:\n'              \
         + yaml.dump(outputs)


def statusLine(url, id, st):
    
    outputsBaseUrl = getBaseUrl(url)
    
    state       = st.v['state']                                if st.isOk() else None
    outputs     = pickUrls(outputsBaseUrl, st.v['outputs'])    if st.isOk() else None
    
    return '  '.join([url, id, state])  \
       + (f'\n{formatOutputs(outputs)}' if outputs else '')


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
        
        url = site['url']
        id = site['id']
        
        st = info(url, id)
        
#        pprint(st.v)   # DEBUG
        
        s = statusLine(url, id, st)
        
        print(s)
        
    
    if failures:
        
        print()
        print('Failures:')
            
        for site in failures:
            
            print(f"{site['url']}  {site['error']}")
        
    
    



