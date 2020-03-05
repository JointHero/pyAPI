#!/usr/bin/env python

import os
from meta import dbMeta
from sqlalchemy import MetaData
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker, scoped_session
from fastapi.encoders import jsonable_encoder
from config import config
from crud import dbengine
from util import toolkit,log

'''logging'''
log = log.Logger(level=config.app_config['log_level'])

def delete_table(tablename, filter=None, filterparam=None):
    log.logger.debug('delete_table():')
    log.logger.debug('tablename: %s' % tablename)
    log.logger.debug('filter: %s' % filter)
    log.logger.debug('filterparam: %s' % filterparam)
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
        session_factory = sessionmaker(bind=engine)
        scsession = scoped_session(session_factory)
        session = scsession(autoflush=True, autocommit=True)
        delete_st = table.delete()
        log.logger.debug('SQL of Delete: [ %s ]' % delete_st)
        if filter is not None:
            delete_st = delete_st.where(text(filter))
            filterparamdict = toolkit.to_dict(filterparam)
            if filterparamdict is not None:
                result = session.execute(delete_st,filterparamdict)
                log.logger.debug('Delete Result: [ %s ]' % result)
                return_json['delet_rowcount'] = result.rowcount
            else:
                return_json['delet_rowcount'] = 0
        else:
            return_json['delet_rowcount'] = 0
        return jsonable_encoder(return_json)
    except Exception as e:
        log.logger.error('Exception at crud.delete delete_table(): %s ' % e)
    finally:
        session.close()
        scsession.remove()

def delete_table_by_id(tablename, idfiled=None, idvalue=None):
    log.logger.debug('delete_table_by_id():')
    log.logger.debug('tablename: %s' % tablename)
    log.logger.debug('idfiled: %s' % idfiled)
    log.logger.debug('idvalue: %s' % idvalue)
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
        session_factory = sessionmaker(bind=engine)
        scsession = scoped_session(session_factory)
        session = scsession(autoflush=True, autocommit=True)
        lpklist = []
        if idfiled is not None:
            lpklist = toolkit.to_list(idfiled)
        else:
            lpklist = dbMeta.DBMeta().gettablekey(tablename)
        pkstr = None
        for pk in lpklist:
            if pkstr is not None:
                pkstr = pkstr + ' and ' + pk + '=:' + pk
            else:
                pkstr = pk + '=:' + pk
        log.logger.debug('Primarykey select string : [ %s ]' % pkstr)
        pkparm = dict(zip(lpklist, toolkit.to_list(idvalue)))
        typedpkparm = {}
        for (k, v) in pkparm.items():
            typedpkparm[k] = table.c[k].type.python_type(v)
        log.logger.debug('Primarykey select param : [ %s ]' % typedpkparm)
        delete_st = table.delete()
        if pkstr is not None:
            log.logger.debug('SQL of Delete: [ %s ]' % delete_st)
            delete_st = delete_st.where(text(pkstr))
            if len(typedpkparm) >= len(lpklist):
                result = session.execute(delete_st,typedpkparm)
                log.logger.debug('Delete Result: [ %s ]' % result)
                return_json['delet_rowcount']=result.rowcount
            else:
                return_json['delet_rowcount'] = 0

        return jsonable_encoder(return_json)
    except Exception as e:
        log.logger.error('Exception at crud.delete delete_table_by_id(): %s ' % e)
    finally:
        session.close()
        scsession.remove()




if __name__ == '__main__':
    print(delete_table_by_id('test', 'id', '56'))