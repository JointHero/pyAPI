#!/usr/bin/env python
from config import config
from meta import dbMeta
from fastapi.encoders import jsonable_encoder
from sqlalchemy import inspect, create_engine, MetaData, Table
uri = config.db_config['uri']
engine = create_engine(uri, echo=False)
inspector = inspect(engine)
schemas = inspector.get_schema_names()
default_schema = inspector.default_schema_name
metadata = MetaData()
metadata.reflect(bind=engine, schema=default_schema, views=True)
print("Schema: %s" % default_schema)
for table_name in inspector.get_table_names(schema=default_schema):
    print("    Table: %s" % table_name)
    pk = inspector.get_pk_constraint(table_name,schema=default_schema)
    print("        PrimaryKey: name=%s, constrained_columns=%s" % (pk['name'],pk['constrained_columns']))
    for index in inspector.get_indexes(table_name,schema=default_schema):
        print("        Index: %s" % index)
    for column in inspector.get_columns(table_name,schema=default_schema):
        print("        Column: %s" % column)
for view_name in inspector.get_view_names(schema=default_schema):
    print("    View: %s" % view_name)
    print("    ViewDefine: %s" % inspector.get_view_definition(view_name, schema=default_schema))
    for table_v in reversed(metadata.sorted_tables):
        if table_v.key == default_schema+'.'+view_name:
            for v_column_name in table_v.columns:
                print("        View ColumnName: %s - %s - %s - %s" % (v_column_name.name,v_column_name.type.__str__,v_column_name.default,v_column_name.nullable))

'''
print("="*50)
for schema in schemas:
    print("Schema: %s" % schema)
    if schema == default_schema:
        metadata.reflect(bind=engine, schema=schema, views=True)
        for table_name in reversed(metadata.sorted_tables):
            print("TableName: %s" % table_name)
            for column_name in table_name.columns:
                print("    ColumnName: %s" % column_name)


for schema in schemas:
    print("schema: %s" % schema)
    for table_name in inspector.get_table_names(schema=schema):
        print("table: %s" % table_name)
        for column in inspector.get_columns(table_name, schema=schema):
            print("Column: %s" % column)
'''



'''
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey,inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

uri = 'mysql+pymysql://root:passw0rd@192.168.10.15:23306/acmondb'
engine = create_engine(uri, echo=False)
session = sessionmaker(bind=engine)
metadata = MetaData(bind=engine)
metadata.reflect(bind=engine)
print(metadata.tables.keys())
Base = automap_base(metadata=metadata)
Base.prepare()
print(Base.classes)
for cl in Base.classes:
    print(cl)
#for tn in metadata.tables.keys():

inspector = inspect(engine)
schemas = inspector.get_schema_names()
for schema in schemas:
    print("schema: %s" % schema)
    for table_name in inspector.get_table_names(schema=schema):
        print("table: %s" % table_name)
        for column in inspector.get_columns(table_name, schema=schema):
            print("Column: %s" % column)
'''

