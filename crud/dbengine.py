#!/usr/bin/env python

import os
from config import config
from sqlalchemy import create_engine
from util import toolkit,log

'''logging'''
log = log.Logger(level=config.app_config['log_level'])

def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class DBEngine(object):
    def __init__(self):
        uri = ''
        if config.db_config['gendburi']:
            uri = str(toolkit.gen_dburi())+'/'+config.db_config['dbname']
        else:
            uri = config.db_config['dburi']
        log.logger.debug('Connect use uri [ %s ]' % uri)
        self.__engine = create_engine(uri,
                                      echo=False,
                                      pool_size=config.db_config['pool_size'],
                                      max_overflow=config.db_config['max_overflow'],
                                      pool_use_lifo=config.db_config['pool_use_lifo'],
                                      pool_pre_ping=config.db_config['pool_pre_ping'],
                                      pool_recycle=config.db_config['pool_recycle'])

    def getengine(self):
        return self.__engine
