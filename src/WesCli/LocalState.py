# encoding: utf-8

import json
from WesCli.either import Either
import os
from WesCli.exception import UserMessageException


DOT_FILE = os.path.join(os.environ.get('HOME'), '.config/WesCli/state')
        

class LocalState(object):
    '''
    Workflow url
    List:
        Site (wes base url)
        inputTemplateParams    TODO?
        runId
    '''
    
    def __init__(self, workflowUrl):
         
        self.workflowUrl = workflowUrl
        self.sites = []
        
    
    def add(self, url
                , idOrError: Either): 
        
        s = {
            
            'url'  : url
           ,'ok'   : True
           ,'id'   : idOrError.v
        
        } if idOrError.isOk() else {
            
            'url'   : url     
           ,'ok'    : False
           ,'error' : idOrError.v
        } 
        
        self.sites.append(s)
        

    def createConfigFolderIfNecessary(self):
        
        folder = os.path.dirname(DOT_FILE)
        if not os.path.exists(folder):
            os.mkdir(folder)


    def save(self):
        
        # The 1st time, the directory might not exist
        self.createConfigFolderIfNecessary()
        
        with open(DOT_FILE, 'w') as f:
        
            json.dump(self.asDict(), f)
        
            
    def load(self):
        
        if not os.path.exists(DOT_FILE):
            
            raise UserMessageException("Local state file not found. Have you ran 'wes run' before?")
        
            
        with open(DOT_FILE) as f:
        
            d = json.load(f)
            
            self.workflowUrl = d['workflowUrl']
            self.sites       = d['sites']
            

    def asDict(self):
        
        return {
            
            'workflowUrl'   : self.workflowUrl 
           ,'sites'         : self.sites
        }


    def __repr__(self):
        
        return str(self.asDict())

