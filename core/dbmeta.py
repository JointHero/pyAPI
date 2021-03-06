#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from core import dbengine,tableschema
from sqlalchemy import inspect, MetaData
import simplejson as json
from sqlalchemy.ext.declarative import declarative_base
from config import config
from util import log
import pickle

'''config'''
cfg = config.Config()

'''logging'''
log = log.Logger(level=cfg.application['app_log_level'])

# cache file define
metadata_pickle_filename = cfg.schema['schema_cache_filename']
cache_path = os.path.join(os.path.expanduser("~"), ".pyAPI_cache")

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
        self.use_schema = cfg.database['db_use_schema']
        self.__schema = cfg.database['db_schema']
        self.__tableCount = 0
        self.__tables = 'N/A'
        self.__viewCount = 0
        self.__metadata = None
        self.load_metadata()
        if os.path.exists(self.get_schema_file()) and cfg.application['app_force_generate_meta'] == False:
            log.logger.debug('Schema file exists, you can load it to application ...')
        else:
            log.logger.debug('Schema file does not exists, generate it from database ...')
            self.gen_schema()
        self.load_schema()


    def load_metadata(self):
        engine = dbengine.DBEngine().getengine()
        cached_metadata = None
        if cfg.schema['schema_cache_enabled'] == True:
            if os.path.exists(os.path.join(cache_path, metadata_pickle_filename)):
                try:
                    with open(os.path.join(cache_path, metadata_pickle_filename), 'rb') as cache_file:
                        cached_metadata = pickle.load(file=cache_file)
                        log.logger.debug('Metadata cache exists, load meta from cache file [ %s ]' % os.path.join(cache_path, metadata_pickle_filename))
                except IOError:
                    # cache file not found - no problem, reflect as usual
                    log.logger.debug('Metadata cache does not exists, will generate it from database ...')
            if cached_metadata:
                cached_metadata.bind = engine
                self.__metadata = cached_metadata
            else:
                metadata = MetaData(bind=engine)
                if self.use_schema:
                    metadata = MetaData(bind=engine, schema=self.__schema)
                if cfg.schema['schema_fetch_all_table'] == True:
                    metadata.reflect(views=True)
                else:
                    metadata.reflect(views=True, only=cfg.schema['schema_fetch_tables'])
                try:
                    if not os.path.exists(cache_path):
                        os.makedirs(cache_path)
                    with open(os.path.join(cache_path, metadata_pickle_filename), 'wb') as cache_file:
                        pickle.dump(metadata, cache_file)
                        log.logger.debug('Metadata cache save to [ %s ] ' % os.path.join(cache_path, metadata_pickle_filename))
                except:
                    # couldn't write the file for some reason
                    log.logger.debug('Metadata save Error [ %s ] ' % os.path.join(cache_path, metadata_pickle_filename))
                self.__metadata = metadata
        else:
            metadata = MetaData(bind=engine)
            if self.use_schema:
                metadata = MetaData(bind=engine, schema=self.__schema)
            if cfg.schema['schema_fetch_all_table'] == True:
                metadata.reflect(views=True)
            else:
                metadata.reflect(views=True, only=cfg.schema['schema_fetch_tables'])
            self.__metadata = metadata

    def getmetadata(self):
        if self.__metadata is not None:
            return self.__metadata
        else:
            return None

    def get_schema_file(self):
        basepath = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        apppath = os.path.abspath(os.path.join(basepath,os.pardir))
        configpath = os.path.abspath(os.path.join(apppath,'config'))
        metafilepath = os.path.abspath(os.path.join(configpath,cfg.schema['schema_db_metafile']))
        return metafilepath

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

    def load_schema(self):
        log.logger.debug('Loading schema from %s' % self.get_schema_file())
        with open(self.get_schema_file(),'r') as metafile:
            jmeta = json.loads(metafile.read())
            self.__schema=jmeta['Schema']
            if len(jmeta['Tables']) > 0:
                self.__tables = []
                for jtbname in jmeta['Tables']:
                    jtable = jmeta['Tables'][jtbname]
                    table = tableschema.TableSchema(jtable['Name'], jtable['Type'])
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
        log.logger.debug('Schema load with [ %s ] tables and [ %s ] views' % (self.__tableCount,self.__viewCount ))

    def gen_schema(self):
        engine = dbengine.DBEngine().getengine()
        inspector = inspect(engine)
        metadata = self.getmetadata()
        try:
            if metadata is not None:
                log.logger.debug("Generate Schema from : [ %s ] with db schema [ %s ]" % (cfg.database['db_name'],self.__schema))
                jmeta = {}
                jmeta['Schema'] = cfg.database['db_schema']
                jtbls = {}
                jmeta['Tables'] = jtbls
                table_list_set = set(cfg.schema['schema_fetch_tables'])
                table_names = inspector.get_table_names()
                if self.use_schema:
                    table_names =  inspector.get_table_names(schema=self.__schema)
                for table_name in table_names:
                    persist_table = False
                    if cfg.schema['schema_fetch_all_table'] == True:
                        persist_table = True
                    else:
                        if table_name in table_list_set:
                            persist_table = True
                    if persist_table == True:
                        jtbl = {}
                        jtbls[table_name] = jtbl
                        jtbl['Name'] = table_name
                        jtbl['Type'] = 'table'
                        pk = inspector.get_pk_constraint(table_name)
                        if self.use_schema:
                            pk = inspector.get_pk_constraint(table_name, schema=self.__schema)
                        if len(pk) > 0:
                            jtbl['PrimaryKeys'] = pk['constrained_columns']
                        else:
                            jtbl['PrimaryKeys'] = []
                        jtbl['Indexes'] = inspector.get_indexes(table_name)
                        if self.use_schema:
                            jtbl['Indexes'] = inspector.get_indexes(table_name, schema=self.__schema)
                        jtbl['Columns'] = []
                        table_columes = inspector.get_columns(table_name)
                        if self.use_schema:
                            table_columes = inspector.get_columns(table_name, schema=self.__schema)
                        for column in table_columes:
                            if len(column) > 0:
                                jtbl['Columns'].append({'name': column['name'], 'type': type(column['type']).__name__,
                                                        'default': column['default'], 'nullable': column['nullable']})
                view_names = inspector.get_view_names()
                if self.use_schema:
                    view_names = inspector.get_view_names(schema=self.__schema)
                for view_name in view_names:
                    persist_table = False
                    if cfg.schema['schema_fetch_all_table'] == True:
                        persist_table = True
                    else:
                        if view_name in table_list_set:
                            persist_table = True
                    if persist_table == True:
                        for table_v in reversed(metadata.sorted_tables):
                            if table_v.name == view_name:
                                vtbl = {}
                                jtbls[view_name] = vtbl
                                vtbl['Name'] = view_name
                                vtbl['Type'] = 'view'
                                vtbl['Columns'] = []
                                for v_column_name in table_v.columns:
                                    if len(column) > 0:
                                        vtbl['Columns'].append({'name': v_column_name.name,
                                                                'type': type(column['type']).__name__,
                                                                'default': v_column_name.default,
                                                                'nullable': v_column_name.nullable})
                with open(self.get_schema_file(), 'w') as jsonfile:
                    json.dump(jmeta, jsonfile, separators=(',', ':'), sort_keys=False, indent=4 * ' ', encoding='utf-8')

            else:
                log.logger.error('Can not get metadata at genschema() ... ')
                raise Exception('Can not get metadata at genschema()')
        except Exception as err:
            log.logger.error('Exception get metadata at genschema() %s ' % err)

    def response_schema(self):
        tblist = []
        for tb in self.__tables:
            tblist.append(tb.getname())
        return tblist

    def response_table_schema(self, tablename):
        tb = self.gettable(tablename)
        if tb is not None:
            return tb.table2json()
        else:
            return {}

    def check_table_schema(self, tablename):
        tb = self.gettable(tablename)
        if tb is not None:
            return True
        else:
            return False


if __name__ == '__main__':
    dbmeta = DBMeta()
    metadata = dbmeta.getmetadata()
    if metadata is not None:
        for item in dir(metadata):
            log.logger.debug(item)
        for table in metadata.sorted_tables:
            log.logger.debug(table.name)
    log.logger.debug(dbmeta.get_schema_file())

