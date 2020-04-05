#!/usr/bin/env python

from config import config
from util import log
from core import security, dbengine, pytable, apimodel, userfunc

'''config'''
cfg = config.Config()

'''logging'''
log = log.Logger(level=cfg.application['app_log_level'])
ptable = pytable.Table('test')
log.logger.info('= '*50)
log.logger.info('Query from table test')
log.logger.info('* '*50)
log.logger.info(ptable.select('*','id=:id and name=:name',{'id':3,'name':'sdf'},10,0,'name desc','name',False,True))
log.logger.info('* '*50)
log.logger.info(ptable.selectbyid('3'))

log.logger.info('= '*50)
log.logger.info('Insert into table test')
for n in range(5):
    log.logger.info('* '*50)
    log.logger.info(ptable.insert('id', '{\'name\':\'single\',\'phone\':\'phonnum-123\'}'))
for n in range(5):
    log.logger.info('* '*50)
    log.logger.info(ptable.insert('id', '[{\'name\':\'multiple1\',\'phone\':\'mphone-123\'},{\'name\':\'multiple2\',\'phone\':\'mphone-345\'}]'))

log.logger.info('= '*50)
log.logger.info('Update record in table test')
for n in range(5):
    log.logger.info('* '*50)
    log.logger.info(ptable.updatebyid('id', 120,'{\'name\':\'newname%s\'}'%n))
for n in range(5):
    log.logger.info('* '*50)
    log.logger.info(ptable.update('name=:pname', {'pname':'newname'}, '{\'name\':\'new-name\',\'phone\':\'mphon-e-345\'}'))

log.logger.info('= '*50)
log.logger.info('Delete record in table test')
for n in range(3):
    log.logger.info('* '*50)
    log.logger.info(ptable.deletebyid('id', 130+n))
log.logger.info('* '*50)
log.logger.info(ptable.delete(filter='name=:pname', filterparam='{\'pname\':\'single\'}'))

