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

log.logger.info('= '*50)
log.logger.info('Query from table test')
log.logger.info('* '*50)
log.logger.info(query.query_table('test','*','id=:id and name=:name',{'id':3,'name':'sdf'},10,0,'name desc','name',False,True))
log.logger.info('* '*50)
log.logger.info(query.query_table_byid('test','3'))

log.logger.info('= '*50)
log.logger.info('Insert into table test')
for n in range(5):
    log.logger.info('* '*50)
    log.logger.info(insert.post_table('test', id, '{\'name\':\'single\',\'phone\':\'phonnum-123\'}'))
for n in range(5):
    log.logger.info('* '*50)
    log.logger.info(insert.post_table('test', id, '[{\'name\':\'multiple1\',\'phone\':\'mphone-123\'},{\'name\':\'multiple2\',\'phone\':\'mphone-345\'}]'))

log.logger.info('= '*50)
log.logger.info('Update record in table test')
for n in range(5):
    log.logger.info('* '*50)
    log.logger.info(update.put_table_by_id('test', 'id', 120,'{\'name\':\'newname%s\'}'%n))
for n in range(5):
    log.logger.info('* '*50)
    log.logger.info(update.put_table('test', 'name=:pname', {'pname':'newname'}, '{\'name\':\'new-name\',\'phone\':\'mphon-e-345\'}'))

log.logger.info('= '*50)
log.logger.info('Delete record in table test')
for n in range(3):
    log.logger.info('* '*50)
    log.logger.info(delete.delete_table_by_id('test', 'id', 130+n))
log.logger.info('* '*50)
log.logger.info(delete.delete_table('test', filter='name=:pname', filterparam='{\'pname\':\'single\'}'))

