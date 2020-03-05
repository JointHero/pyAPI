#!/usr/bin/env python

from meta import dbMeta
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from fastapi.encoders import jsonable_encoder
from crud import dbengine
from config import config
from util import toolkit,log

'''logging'''
log = log.Logger(level=config.app_config['log_level'])

def post_table(tablename, idfiled=None, fieldvalue=None):
    log.logger.debug('post_table():')
    log.logger.debug('tablename: %s' % tablename)
    log.logger.debug('idfiled: %s' % idfiled)
    log.logger.debug('fieldvalue: %s' % fieldvalue)
    try:
        return_json= {}
        engine = dbengine.DBEngine().getengine()
        metadata = dbMeta.DBMeta().getmeta()
        if metadata is not None:
            log.logger.debug('metadata exists ....')
        else:
            log.logger.debug('metadata not exists, reflecting ....')
            metadata = MetaData(bind=engine)
            metadata.reflect(views=True)
        table = metadata.tables[tablename]
        log.logger.debug('Table Columns: %s' % table.c)
        insert_st = table.insert()
        log.logger.debug('SQL of Insert: [ %s ]' % insert_st)
        session_factory = sessionmaker(bind=engine)
        scsession = scoped_session(session_factory)
        session = scsession(autoflush=True, autocommit=True)
        fvl = toolkit.to_fvcol(fieldvalue)
        log.logger.debug('Insert Values: [ %s ]' % fvl)
        if fvl is not None:
            result = session.execute(insert_st,fvl)
            log.logger.debug('Insert Result: [ %s ]' % result)
            return_json['insert_row_id']=result.lastrowid
        else:
            return_json['insert_row_id'] = -1
        return jsonable_encoder(return_json)
    except Exception as e:
        log.logger.error('Exception at crud.insert post_table(): %s ' % e)
    finally:
        session.close()
        scsession.remove()




if __name__ == '__main__':
    post_table('test', id, '{\'name\':\'sdf\',\'phone\':\'234243\'}')