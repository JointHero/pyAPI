#!/usr/bin/env python

import os
from config import config
from meta import dbTable
from meta import dbMeta
from sqlalchemy import inspect, create_engine, MetaData, Table
from typing import List, Optional, Generic, TypeVar, Type
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, scoped_session
from fastapi.encoders import jsonable_encoder
from crud import dbengine
import simplejson as json
import re
import logging

'''logging'''
logger = logging.getLogger("query")

def query_table(tablename, fields='*', filter=None, limit=10, offset=0, order=None, group=None, count_only=False, include_count=False, ids=None, id_field=None):
    try:
        engine = dbengine.DBEngine().getengine()
        metadata = dbMeta.DBMeta().getmeta()
        if metadata is not None:
            logger.debug('metadata exists ....')
        else:
            logger.debug('metadata not exists, reflecting ....')
            metadata = MetaData(bind=engine)
            metadata.reflect(views=True)
        table = metadata.tables[tablename]
        logger.debug(table.c)
        session_factory = sessionmaker(bind=engine)
        scsession = scoped_session(session_factory)
        session = scsession()
        select_cl = []
        if fields == '*':
            print('*')
            select_st = select([table])
        else:
            fieldlist = re.split(r'[\s\,\;]+', fields)
            for cl in table.c:
                if cl.name in fieldlist:
                    select_cl.append(cl)
            select_st = select(select_cl)
        select_st = select_st.limit(limit).offset(offset)
        logger.debug(select_st)
        result = session.execute(select_st)
        d, a = {}, []
        for row in result:
            # result.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in row.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)
        return jsonable_encoder(a)
    except Exception as e:
        logger.exception('Exception at crud.query query(): ', e)
    finally:
        session.close()
        scsession.remove()





if __name__ == '__main__':
    print(query_table('faultmsg','fcarriageno,fmsgtype'))
