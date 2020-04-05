#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import config_with_yaml as config

def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Config(object):
    def __init__(self):
        CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
        cfg = config.load(os.path.join(CONFIG_DIR, 'config.yml'))
        self.application = cfg.getProperty('application')
        self.schema = cfg.getProperty('schema')
        self.query = cfg.getProperty('query')
        self.security = cfg.getProperty('security')
        self.database = cfg.getProperty('database')
        self.connection = cfg.getProperty('connection')

if __name__ == '__main__':
    print(Config().application)
    print(Config().schema)
    print(Config().query)
    print(Config().security)
    print(Config().database)
    print(Config().connection)