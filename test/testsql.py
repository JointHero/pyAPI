#!/usr/bin/env python
from config import config
from meta import dbMeta
from sqlalchemy import inspect, create_engine, MetaData, Table
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, scoped_session
from meta import dbMeta as meta
from meta import dbTable as table
import simplejson as json
import logging
from crud import dbengine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from fastapi.encoders import jsonable_encoder

'''logging'''
logger = logging.getLogger("dbMeta")


uri = config.db_config['uri']
engine = create_engine(uri, echo=False, pool_size=20, max_overflow=0)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

'''
connection = engine.connect()
result = connection.execute("select * from faultmsg limit 100")
for row in result:
    print("row:", row)
connection.close()
'''
result = engine.execute("select * from faultmsg limit 100")
#for row in result:
#    print("row:", row)
'''
aa = '/api/v1'
if aa.startswith('/'):
    #print('yes')
    pass

meta = meta.DBMeta()
tables = meta.gettables()
tblist = []
print(json.dumps(tblist))
for tb in tables:
    tblist.append(tb.getname())
print(json.dumps(tblist))

#print(json.dumps(meta.gettable('faultmsg'), default=lambda obj: obj.__dict__))

print(meta.response_table_schema('faultmsg'))
logger.debug(meta.response_schema())

#print(meta.gettables())
'''
engine = dbengine.DBEngine().getengine()
#metadata = MetaData(bind=engine)
#metadata.reflect(views=True)
metadata = dbMeta.DBMeta().getmeta()
if metadata is not None:
    logger.debug('metadata exists ....')
else:
    logger.debug('metadata not exists, reflecting ....')
    metadata = MetaData(bind=engine)
    metadata.reflect(views=True)
table = metadata.tables['faultmsg']
print(table.c)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

select_st = select([table.c.fmsgtype,table.c.parsetime]).limit(5).offset(300000)
#print(select_st)
result=session.execute(select_st)
d, a = {}, []
for row in result:
    # result.items() returns an array like [(key0, value0), (key1, value1)]
    for column, value in row.items():
        # build up the dictionary
        d = {**d, **{column: value}}
    a.append(d)
print(a)
session.close()
Session.remove()
'''
result = session.query(metadata.tables['v_faultmsg']).all()
d, a = {}, []
for row in result:
    print(row)
    # result.items() returns an array like [(key0, value0), (key1, value1)]
    #for column, value in row.items():
        # build up the dictionary
    #    d = {**d, **{column: value}}
    #a.append(d)
print(a)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
Base = declarative_base()


print(metadata.tables['faultmsg'])

class faultmsg_t(Base):
    __tablename__ = 'faultmsg'
    fcarriageno = Column(String, primary_key=True)
    fmsgtype = Column(String)

fm = session.query(metadata.tables['faultmsg']).first()
print(fm)
print(jsonable_encoder(fm))
session.close()
Session.remove()

metadata = MetaData()
metadata.reflect(bind=engine)
print(metadata.tables['faultmsg'])

table=meta.DBMeta().gettable('faultmsg')
#print(table.getcolumns())
'''