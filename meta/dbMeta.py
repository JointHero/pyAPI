#!/usr/bin/env python

import os
from crud import dbengine
from meta import dbTable
from sqlalchemy import inspect, MetaData
import simplejson as json
import re
from config import config
from util import log

'''logging'''
log = log.Logger(level=config.app_config['log_level'])

def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class DBMeta(object):
    def __init__(self):
        self.__schema = 'N/A'
        self.__tableCount = 0
        self.__tables = 'N/A'
        self.__viewCount = 0
        self.__metadata = None
        self.load_activemeta()
        self.check_meta()
        self.load_meta()

    def load_activemeta(self):
        engine = dbengine.DBEngine().getengine()
        metadata = MetaData(bind=engine)
        metadata.reflect(views=True)
        self.__metadata = metadata

    def getmeta(self):
        if self.__metadata is not None:
            log.logger.debug(self.__metadata)
            return self.__metadata

    def getschema(self):
        return self.__schema

    def gettablecount(self):
        return self.__tableCount

    def gettables(self):
        return self.__tables

    def gettable(self,tablename):
        if len(self.__tables) > 0:
            for table in self.__tables:
                if table.getname() == tablename:
                    return table
        else:
            return None

    def gettablekey(self,tablename):
        table = self.gettable(tablename)
        if table is not None:
            pks = table.getprimarykeys()
            if pks == 'N/A':
                pks = []
            return pks
        else:
            return None

    def getviewcount(self):
        return self.__viewCount

    def get_meta_file(self):
        return os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + '..'+os.path.sep+'config'),config.app_config['metafile'])

    def load_meta(self):
        with open(self.get_meta_file(),'r') as metafile:
            jmeta = json.loads(metafile.read())
            self.__schema=jmeta['Schema']
            if len(jmeta['Tables']) > 0:
                self.__tables = []
                for jtbname in jmeta['Tables']:
                    jtable = jmeta['Tables'][jtbname]
                    table = dbTable.DBTable(jtable['Name'],jtable['Type'])
                    for elename in jtable:
                        if elename == 'PrimaryKeys':
                            table.setprimarykeys(jtable[elename])
                        elif elename == 'Indexes':
                            table.setindexes(jtable[elename])
                        elif elename == 'Columns':
                            table.setcolumns(jtable[elename])
                    self.__tables.append(table)
                    if table.gettype() == 'table':
                        self.__tableCount = self.__tableCount + 1
                    if table.gettype() == 'view':
                        self.__viewCount = self.__viewCount + 1

    def check_meta(self):
        if os.path.exists(self.get_meta_file()) and config.app_config['forcegenmeta'] == False:
            log.logger.debug('Metafile exists, you can load it to application ...')
        else:
            log.logger.debug('Metafile does not exists, generate it from database ...')
            engine = dbengine.DBEngine().getengine()
            inspector = inspect(engine)
            #metadata = MetaData()
            #metadata.reflect(bind=engine, schema=config.db_config['dbname'], views=True)
            metadata = self.getmeta()
            if metadata is not None:
                log.logger.debug('metadata exists ....')
                metadata = MetaData(bind=engine, schema=config.db_config['dbname'])
                metadata.reflect(views=True)
            else:
                log.logger.debug('metadata not exists, reflecting ....')
                metadata = MetaData(bind=engine, schema=config.db_config['dbname'])
                metadata.reflect(views=True)
            log.logger.debug("Read Schema: [ %s ]" % config.db_config['dbname'])
            pattern = re.compile("'(.*)'")
            jmeta = {}
            jmeta['Schema'] = config.db_config['dbname']
            jtbls = {}
            jmeta['Tables'] = jtbls
            for table_name in inspector.get_table_names(schema=config.db_config['dbname']):
                jtbl = {}
                jtbls[table_name]=jtbl
                jtbl['Name'] = table_name
                jtbl['Type'] = 'table'
                pk = inspector.get_pk_constraint(table_name, schema=config.db_config['dbname'])
                if len(pk) > 0:
                    jtbl['PrimaryKeys'] = pk['constrained_columns']
                else:
                    jtbl['PrimaryKeys'] = []
                jtbl['Indexes'] = inspector.get_indexes(table_name, schema=config.db_config['dbname'])
                jtbl['Columns'] = []
                for column in inspector.get_columns(table_name, schema=config.db_config['dbname']):
                    if len(column) > 0:
                        jtbl['Columns'].append({'name':column['name'], 'type': pattern.findall(str(column['type'].python_type))[0], 'default':column['default'], 'nullable':column['nullable']})
            for view_name in inspector.get_view_names(schema=config.db_config['dbname']):
                #metadata.reflect(bind=engine, schema=config.db_config['dbname'], views=True)
                for table_v in reversed(metadata.sorted_tables):
                    if table_v.key == config.db_config['dbname'] + '.' + view_name:
                        vtbl = {}
                        jtbls[view_name] = vtbl
                        vtbl['Name'] = view_name
                        vtbl['Type'] = 'view'
                        vtbl['Columns'] = []
                        for v_column_name in table_v.columns:
                            if len(column) > 0:
                                vtbl['Columns'].append({'name':v_column_name.name, 'type': pattern.findall(str(v_column_name.type.python_type))[0], 'default':v_column_name.default, 'nullable':v_column_name.nullable})
            with open(self.get_meta_file(), 'w') as jsonfile:
                json.dump(jmeta, jsonfile, separators=(',', ':'), sort_keys=False, indent=4 * ' ', encoding='utf-8')

    def response_schema(self):
        tblist = []
        for tb in self.__tables:
            tblist.append(tb.getname())
        return tblist

    def response_table_schema(self,tablename):
        tb = self.gettable(tablename)
        if tb is not None:
            return tb.table2json()
        else:
            return {}
    
    def check_table_schema(self,tablename):
        tb = self.gettable(tablename)
        if tb is not None:
            return True
        else:
            return False

if __name__ == '__main__':
    dbmeta = DBMeta()
    print(dbmeta.getviewcount())
    print(dbmeta.check_table_schema('faultmsg'))