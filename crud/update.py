#!/usr/bin/env python


from config import config
from meta import dbMeta
from sqlalchemy import MetaData
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker, scoped_session
from fastapi.encoders import jsonable_encoder
from crud import dbengine
from util import toolkit,log

'''logging'''
log = log.Logger(level=config.app_config['log_level'])

def put_table(tablename, filter=None, filterparam=None, fieldvalue=None):
    log.logger.debug('put_table():')
    log.logger.debug('tablename: %s' % tablename)
    log.logger.debug('filter: %s' % filter)
    log.logger.debug('filterparam: %s' % filterparam)
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
        session_factory = sessionmaker(bind=engine)
        scsession = scoped_session(session_factory)
        session = scsession(autoflush=True, autocommit=True)
        fvl = toolkit.to_fvcol(fieldvalue)
        log.logger.debug('Update Values: [ %s ]' % fvl)
        update_st = table.update()
        if filter is not None:
            update_st = update_st.where(text(filter))
            if fvl is not None:
                update_st = update_st.values(fvl)
                log.logger.debug('SQL of Update: [ %s ]' % update_st)
                filterparamdict = toolkit.to_dict(filterparam)
                if filterparamdict is not None:
                    result = session.execute(update_st, filterparamdict)
                    log.logger.debug('Update Result: [ %s ]' % result)
                    return_json['udpate_rowcount'] = result.rowcount
                else:
                    return_json['udpate_rowcount'] = 0
            else:
                return_json['udpate_rowcount'] = 0
        else:
            return_json['udpate_rowcount'] = 0
        return jsonable_encoder(return_json)
    except Exception as e:
        log.logger.error('Exception at crud.update put_table(): %s ' % e)
    finally:
        session.close()
        scsession.remove()


def put_table_by_id(tablename, idfiled=None, idvalue=None, fieldvalue=None):
    log.logger.debug('put_table_by_id():')
    log.logger.debug('tablename: %s' % tablename)
    log.logger.debug('idfiled: %s' % idfiled)
    log.logger.debug('idvalue: %s' % idvalue)
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
        lpklist = []
        if idfiled is not None:
            lpklist = toolkit.to_list(idfiled)
        else:
            lpklist = dbMeta.DBMeta().gettablekey(tablename)
        ulpklist = toolkit.uappendlist(lpklist)
        pkstr = None
        for pk in lpklist:
            if pkstr is not None:
                pkstr = pkstr + ' and ' + pk + '=:'+config.app_config['param_prefix'] + pk
            else:
                pkstr = pk + '=:'+config.app_config['param_prefix'] + pk
        log.logger.debug('Primarykey select string : [ %s ]' % pkstr)


        pkparm = dict(zip(lpklist, toolkit.to_list(idvalue)))
        #pkparm = dict(zip(ulpklist, toolkit.to_list(idvalue)))
        typedpkparm = {}
        for (k, v) in pkparm.items():
            typedpkparm[k] = table.c[k].type.python_type(v)
        prlist =  [ v for v in typedpkparm.values() ]
        submittypedpkparm = dict(zip(ulpklist, prlist))
        log.logger.debug('Primarykey select param : [ %s ]' % submittypedpkparm)
        session_factory = sessionmaker(bind=engine)
        scsession = scoped_session(session_factory)
        session = scsession(autoflush=True, autocommit=True)
        fvl = toolkit.to_fvcol(fieldvalue)
        update_st = table.update()
        if pkstr is not None:
            update_st = update_st.where(text(pkstr))
            if fvl is not None:
                update_st = update_st.values(fvl)
                log.logger.debug('SQL of Update: [ %s ]' % update_st)
                if len(submittypedpkparm) >= len(lpklist):
                    result = session.execute(update_st, submittypedpkparm)
                    log.logger.debug('Update Result: [ %s ]' % result)
                    return_json['udpate_rowcount'] = result.rowcount
                else:
                    return_json['udpate_rowcount'] = 0
            else:
                return_json['udpate_rowcount'] = 0
        else:
            return_json['udpate_rowcount'] = 0
        return jsonable_encoder(return_json)
    except Exception as e:
        log.logger.error('Exception at crud.update put_table_by_id(): ', e)
    finally:
        session.close()
        scsession.remove()



if __name__ == '__main__':
    print(put_table_by_id('test', 'id', 35,'{\'name\':\'zhjjj\'}'))
    #print(put_table('test', 'name=:pname', {'pname':'zhjjj'}, '{\'name\':\'zhjjj\',\'phone\':\'232323\'}'))

