#!/usr/bin/env python

import os
from crud import  dbengine, delete, update, insert, query
from meta import dbMeta, dbTable
import simplejson as json
import re
from config import config
from util import toolkit,log

'''logging'''
log = log.Logger(level=config.app_config['log_level'])

dbmeta = dbMeta.DBMeta()
log.logger.info('dbMeta getviewcount: %s' % dbmeta.getviewcount())
log.logger.info('dbMeta gettablecount: %s' % dbmeta.gettablecount())
log.logger.info('dbMeta getmeta: %s' % dbmeta.getmeta())
log.logger.info('dbMeta getschema: %s' % dbmeta.getschema())
log.logger.info('dbMeta gettables: %s' % dbmeta.gettables())
log.logger.info('dbMeta gettable-test: %s' % dbmeta.gettable('test'))
log.logger.info('dbMeta gettablekey-test: %s' % dbmeta.gettablekey('test'))
log.logger.info('dbMeta response_schema: %s' % dbmeta.response_schema())
log.logger.info('dbMeta response_table_schema-test: %s' % dbmeta.response_table_schema('test'))
