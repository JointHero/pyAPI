#!/usr/bin/env python


from config import config
from meta import dbMeta
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, scoped_session
from fastapi.encoders import jsonable_encoder
from crud import dbengine
import re
from util import toolkit,log

'''logging'''
log = log.Logger(level=config.app_config['log_level'])

def query_table(tablename, fieldlist='*', filter=None,
                filterparam=None,
                limit=config.db_config['default_limit'],
                offset=config.db_config['default_offset'],
                order=None, group=None,
                count_only=False, include_count=False):
    log.logger.debug('query_table():')
    log.logger.debug('tablename: %s' % tablename)
    log.logger.debug('fieldlist: %s' % fieldlist)
    log.logger.debug('filter: %s' % filter)
    log.logger.debug('limit: %s' % limit)
    log.logger.debug('offset: %s' % offset)
    log.logger.debug('order: %s' % order)
    log.logger.debug('group: %s' % group)
    log.logger.debug('count_only: %s' % count_only)
    log.logger.debug('include_count: %s' % include_count)
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
        session = scsession()
        select_cl = []
        if fieldlist == '*':
            select_st = select([table])
            #print(next(iter(table.c)))
            count_st = select([func.count(next(iter(table.c))).label('col_count')])
        else:
            field_list = re.split(r'[\s\,\;]+', fieldlist)
            for cl in table.c:
                if cl.name in field_list:
                    select_cl.append(cl)
            select_st = select(select_cl)
            count_st = select([func.count(select_cl[0]).label('col_count')])
        if limit > config.db_config['limit_upset']:
            limit = config.db_config['limit_upset']
        select_st = select_st.limit(limit).offset(offset)
        if order is not None:
            select_st = select_st.order_by(text(order))
        if group is not None:
            select_st = select_st.group_by(text(group))
        #print(select_st)
        #print(count_st)
        log.logger.debug('SQL of Query: [ %s ]' % select_st)
        log.logger.debug('SQL of Count: [ %s ]' % count_st)

        if filter is not None:
            select_st = select_st.where(text(filter))
            count_st = count_st.where(text(filter))
            filterparamdict = toolkit.to_dict(filterparam)
            if filterparamdict is not None:
                result = session.execute(select_st,filterparamdict)
                cresult = session.execute(count_st,filterparamdict)
            else:
                result = None
                cresult = None
        else:
            result = session.execute(select_st)
            cresult = session.execute(count_st)
        log.logger.debug('SQL of Query Full : [ %s ]' % select_st)
        log.logger.debug('SQL of Count Full : [ %s ]' % count_st)

        log.logger.debug('Select Count Result: [ %s ]' % cresult)
        crow = cresult.fetchone()
        colcount=crow['col_count']
        d, a = {}, []
        if result is not None:
            log.logger.debug('Select Result: [ %s ]' % result)
            for row in result:
                # result.items() returns an array like [(key0, value0), (key1, value1)]
                for column, value in row.items():
                    # build up the dictionary
                    d = {**d, **{column: value}}
                a.append(d)
            if bool(count_only):
                return_json['record_count'] =colcount
            elif bool(include_count):
                return_json['record_count'] =colcount
                return_json['data'] =a
            else:
                return_json['data'] = a
        else:
            return_json['data'] = None
        return jsonable_encoder(return_json)
    except Exception as e:
        log.logger.error('Exception at crud.query query_table(): %s ' % e)
    finally:
        session.close()
        scsession.remove()

def query_table_byid(tablename, tbid, fieldlist=None, idfiled=None):
    log.logger.debug('query_table_byid():')
    log.logger.debug('tablename: %s' % tablename)
    log.logger.debug('tbid: %s' % tbid)
    log.logger.debug('fieldlist: %s' % fieldlist)
    log.logger.debug('idfiled: %s' % idfiled)
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
        session = scsession()
        select_cl = []
        if fieldlist is not None:
            if fieldlist == '*':
                select_st = select([table])
            else:
                field_list = toolkit.to_list(fieldlist)
                for cl in table.c:
                    if cl.name in field_list:
                        select_cl.append(cl)
                select_st = select(select_cl)
        else:
            select_st = select([table])
        select_st = select_st.limit(config.db_config['limit_upset'])
        l_pklist = []
        if idfiled is not None:
            l_pklist = toolkit.to_list(idfiled)
        else:
            l_pklist = dbMeta.DBMeta().gettablekey(tablename)
        pkstr = None
        for pk in l_pklist:
            if pkstr is not None:
                pkstr = pkstr + ' and ' + pk + '=:' + pk
            else:
                pkstr = pk + '=:' + pk
        log.logger.debug('Primarykey select string : [ %s ]' % pkstr)
        pkparm = dict(zip(l_pklist, toolkit.to_list(tbid)))
        typedpkparm={}
        for (k,v) in pkparm.items():
            typedpkparm[k]=table.c[k].type.python_type(v)
        log.logger.debug('Primarykey select param : [ %s ]' % typedpkparm)
        # print(pkparm)
        if pkstr is not None:
            select_st = select_st.where(text(pkstr))
            if len(typedpkparm) >= len(l_pklist):
                result = session.execute(select_st, typedpkparm)
            else:
                result = None
        else:
            result = session.execute(select_st)
        log.logger.debug('SQL of Query: [ %s ]' % select_st)
        #print(select_st)
        d, a = {}, []
        if result is not None:
            log.logger.debug('Select Result: [ %s ]' % result)
            for row in result:
                # result.items() returns an array like [(key0, value0), (key1, value1)]
                for column, value in row.items():
                    # build up the dictionary
                    d = {**d, **{column: value}}
                a.append(d)
            return_json['data'] = a
        else:
            return_json['data'] = None
        return jsonable_encoder(return_json)
    except Exception as e:
        log.logger.error('Exception at crud.query query_table_byid(): %s ' % e)
    finally:
        session.close()
        scsession.remove()




if __name__ == '__main__':
    #print(query_table('test','*','id=:id and name=:name',{'id':3,'name':'sdf'},10,0,'name desc','name',False,True))
    #print(query_table('test','id,name','id=:pid and name=:pname',None,10,0,'name desc','name',False,True))

    #print(query_table_byid('test','3'))
    print(query_table_byid('bank_dist', '59', None,'age'))

    #pks = dbMeta.DBMeta().gettablekey('v_faultmsg')
    #print(pks)