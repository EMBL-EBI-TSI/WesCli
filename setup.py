# coding=utf-8

#@PydevCodeAnalysisIgnore
from setuptools import setup, find_packages

setup(
    name = "WesCli",
    version = "1.0",
    packages = find_packages('src'),
    package_dir = {'':'src'},
    

    entry_points = {
        'console_scripts': [
#           'scriptName = my_package.some_module:main_func',
            'wes        = WesCli.Main:entryPoint',
        ],
    }
)
