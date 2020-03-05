#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from loguru import logger


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Logger(object):
    def __init__(self, level='INFO'):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        LOG_PATH = os.path.join(BASE_DIR, 'log')
        #logger.add(sys.stderr, format="{time} {level} {message}", level=level)
        logger.add(os.path.join(LOG_PATH,'api.log'),
                   format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
                   rotation="100 MB",
                   retention="14 days",
                   level=level,
                   enqueue=True)
        self.logger = logger

if __name__ == '__main__':
    log = Logger(level='DEBUG')
    log.logger.info('[测试log] hello, world')
    log.logger.debug('[测试log] hello, world')