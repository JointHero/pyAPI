#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
from util import log
from config import config

'''config'''
cfg = config.Config()

'''logging'''
log = log.Logger(level=cfg.application['app_log_level'])

def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Users(object):
    def __init__(self):
        AUTH_DIR = os.path.dirname(os.path.abspath(__file__))
        try:
            with open(os.path.join(AUTH_DIR, 'users.json'), 'r') as usersfile:
                self.users = json.loads(usersfile.read())
        except Exception as err:
            log.logger.error('Exception load Users file %s ' % err)

if __name__ == '__main__':
    print(Users().users)