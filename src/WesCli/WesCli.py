# encoding: utf-8

import yaml


def loadYaml(filename):
    
    with open(filename, 'r') as f:
        
        return yaml.safe_load(f)

