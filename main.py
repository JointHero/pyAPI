#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
from fastapi import FastAPI, Header, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from config import config, usersdb
from meta import dbMeta as meta
from crud import query, insert, delete, update
from starlette.middleware.cors import CORSMiddleware
from util import toolkit,log
from core import security, apimodel

'''logging'''
log = log.Logger(level=config.app_config['log_level'])

'''api prefix'''
prefix = config.app_config['prefix']
if prefix.startswith('/'):
    pass
else:
    prefix = '/' + prefix
log.logger.info(config.app_config['name'] + 'Start Up ....')
log.logger.info("Api prefix is: [ %s ]" % prefix)

'''API define'''
api = FastAPI(
    title=config.app_config['name'],
    description=config.app_config['description'],
    version=config.app_config['version'],
    openapi_url=prefix+"/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

@api.on_event("startup")
async def startup_event():
    meta.DBMeta()

@api.on_event("shutdown")
def shutdown_event():
    log.logger.info(config.app_config['name'] + 'Shutting Down ....')

'''CORS'''
origins = []

# Set all CORS enabled origins
if config.app_backend_cors_origins:
    origins_raw = config.app_backend_cors_origins.split(",")
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    api.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

'''api route'''

@api.get("/",
         tags=["Default"],
         summary="Get information for this application.",
         description="Return application information",
         )
async def api_root():
    log.logger.debug('Access \'/\' : run in api_root()')
    return {
        "Application_Name":config.app_config['name'],
        "Version": config.app_config['version'],
        "Author":"ibmzhangjun@139.com"
    }

@api.post(prefix +"/token",
          response_model=security.Token,
          tags=["Security"],
          summary="Login to get access token.",
          description="",
          )

async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    log.logger.debug('Access \'/token\' : run in login_for_access_token(), input data username: [%s] and password: [%s]' % (form_data.username, form_data.password))
    user = security.authenticate_user(usersdb.UsersDB().admin_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.app_security['ACCESS_TOKEN_EXPIRE_MINUTES'])
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@api.get(prefix +"/users/me",
         response_model=security.User,
         tags=["Security"],
         summary="Retrieve user infomation.",
         description="",
         )
async def read_users_me(current_user: security.User = Depends(security.get_current_active_user)):
    log.logger.debug('Access \'/users/me/\' : run in read_users_me()')
    return current_user


@api.get(prefix+"/_schema",
         tags=["Schema"],
         summary="Retrieve DbSchema Resources.",
         description="By default, all tables are returned .",
         )
async def get_schema(current_user: security.User = Depends(security.get_current_active_user)):
    log.logger.debug('Access \'/_schema\' : run in get_schema()')

    return meta.DBMeta().response_schema()

@api.get(prefix+"/_schema/{table_name}",
         tags=["Schema"],
         summary="Retrieve table definition for the given table.",
         description="This describes the table, its fields and indexes.",
         )
async def get_table_schema(table_name: str, current_user: security.User = Depends(security.get_current_active_user)):
    log.logger.debug('Access \'/_schema/{table_name}\' : run in get_table_schema(), input data table_name: [%s]' % table_name)
    if not meta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    return meta.DBMeta().response_table_schema(table_name)

@api.get(prefix+"/_table/{table_name}",
         tags=["Data - Table Level"],
         summary="Retrieve one or more records. ",
         description="",
         )
async def get_data(table_name: str,
                   fieldlist: str = Header('*'),
                   filter: str = Header(None),
                   filterparam: str = Header(None),
                   limit: int = Header(config.db_config['default_limit'], gt=0, le=config.db_config['limit_upset']),
                   offset: int = Header(config.db_config['default_offset'], gt=-1),
                   order: str = Header(None),
                   group: str = Header(None),
                   count_only: bool = Header(False),
                   include_count: bool = Header(False),
                   current_user: security.User = Depends(security.get_current_active_user)):
    """
        Parameters

        - **table_name** (path): **Required** - Name of the table to perform operations on.
        - **fieldlist** (header): Optional - Comma-delimited list of properties to be returned for each resource, "*" returns all properties. ex: 'id,name'
        - **filter** (header): Optional - SQL-like filter to limit the records to retrieve. ex: 'id=:qid and name=:qname'
        - **filterparam** (header): Optional - SQL-like parameter of *filter. ex: {'qid':3,'qname':'jack'}
        - **limit** (header): Optional - Set to limit the filter results.
        - **offset** (header): Optional - Set to offset the filter results to a particular record count.
        - **order** (header): Optional - SQL-like order containing field and direction for filter results. ex: 'name ASC'
        - **group** (header): Optional - Comma-delimited list of the fields used for grouping of filter results. ex: 'name'
        - **count-only** (header): Optional , default[False] - Return only the total number of filter results.
        - **include-count** (header): Optional , default[False] - Include the total number of filter results in returned result.
    """

    log.logger.debug(
        'Access \'/_table/{table_name}\' : run in get_data(), input data table_name: [%s]' % table_name)
    log.logger.debug('fieldlist: [%s]' % fieldlist)
    log.logger.debug('filter: [%s]' % filter)
    log.logger.debug('filterparam: [%s]' % filterparam)
    log.logger.debug('limit: [%s]' % limit)
    log.logger.debug('offset: [%s]' % offset)
    log.logger.debug('order: [%s]' % order)
    log.logger.debug('group: [%s]' % group)
    log.logger.debug('count_only: [%s]' % count_only)
    log.logger.debug('include_count: [%s]' % include_count)
    if not meta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    return query.query_table(table_name, fieldlist, filter, toolkit.to_dict(filterparam), limit, offset, order, group, count_only, include_count)

@api.post(prefix+"/_table/{table_name}/query",
          tags=["Data - Table Level"],
         summary="Retrieve one or more records. ",
         description="",
         )
async def query_data(table_name: str, tablequerybody:apimodel.TableQueryBody,
                     current_user: security.User = Depends(security.get_current_active_user)):

    """
        Parameters

        - **table_name** (path): **Required** - Name of the table to perform operations on.
        - **request body: **Required**
        ```
            {
             "fieldlist": "string",  -- Optional - Comma-delimited list of properties to be returned for each resource, "*" returns all properties. ex: 'id,name'
             "filter": "string",  -- Optional - SQL-like filter to limit the records to retrieve. ex: 'id=:qid and name=:qname'
             "filterparam": {},  -- Optional - SQL-like parameter of *filter. ex: {'qid':3,'qname':'jack'}
             "limit": 0,  -- Optional - Set to limit the filter results.
             "offset": 0,  -- Optional - Set to offset the filter results to a particular record count.
             "order": "string",  -- Optional - SQL-like order containing field and direction for filter results. ex: 'name ASC'
             "group": "string",  -- Optional - Comma-delimited list of the fields used for grouping of filter results. ex: 'name'
             "count_only": false,  -- Optional , default[False] - Return only the total number of filter results.
             "include_count": false  -- Optional , default[False] - Include the total number of filter results in returned result.
             }
        ```
    """

    log.logger.debug(
        'Access \'/_table/{table_name}/query\' : run in query_data(), input data table_name: [%s]' % table_name)
    log.logger.debug('body: [%s]' % tablequerybody)
    if not meta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    return query.query_table(table_name,tablequerybody.fieldlist,tablequerybody.filter,
                             tablequerybody.filterparam,tablequerybody.limit,tablequerybody.offset,
                             tablequerybody.order,tablequerybody.group,tablequerybody.count_only,
                             tablequerybody.include_count)

@api.post(prefix+"/_table/{table_name}",
          tags=["Data - Table Level"],
         summary="Create one or more records.",
         description="",
         )
async def post_data(table_name: str, tablepost: apimodel.TablePostBody,
                    current_user_role: bool = Depends(security.get_wirte_permission)):

    """
        Parameters

        - **table_name** (path): **Required** - Name of the table to perform operations on.
        - **request body: Required**
        ```
            {
             "fieldvalue": "string",  -- **Required** - Dict or jason formated fieldname-fieldvalue pair. ex: '[{'name':'jack','phone':'55789'}]'
             "idfield": "string"  -- Optional - Comma-delimited list of the fields used as identifiers. ex: 'id'
             }
        ```
    """

    log.logger.debug(
        'Access \'/_table/{table_name}\' : run in post_data(), input data table_name: [%s]' % table_name)
    log.logger.debug('body: [%s]' % tablepost)
    if not meta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    return insert.post_table(table_name, tablepost.idfield, tablepost.fieldvalue)

@api.put(prefix+"/_table/{table_name}",
         tags=["Data - Table Level"],
         summary="Update (replace) one or more records.",
         description="",
         deprecated=False
         )
async def put_data(table_name: str, tableput:apimodel.TablePutBody,
                current_user_role: bool = Depends(security.get_wirte_permission)):

    """
        Parameters

        - **table_name** (path): **Required** - Name of the table to perform operations on.
        - **request body: Required**
        ```
            {
             "filter": "string",  -- Optional - SQL-like filter to limit the records to retrieve. ex: 'id=:qid and name=:qname'
             "filterparam": {},  -- Optional - SQL-like parameter of *filter. ex: {'qid':3,'qname':'jack'}
             "fieldvalue": "string"  -- Optional - Dict or jason formated fieldname-fieldvalue pair. ex: '{'name':'jack','phone':'55789'}'
             }
        ```
        - **Note:** The param name in filter and filterparam **MUST NOT** equal the fieldname !
        - ex: 'id=:id' filter and  {'id':3} in filterparam will is **NOT PERMITTED** !
    """
    log.logger.debug(
        'Access \'/_table/{table_name}\' : run in put_data(), input data table_name: [%s]' % table_name)
    log.logger.debug('body: [%s]' % tableput)
    if not meta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    return update.put_table(table_name, tableput.filter, tableput.filterparam, tableput.fieldvalue)

@api.delete(prefix+"/_table/{table_name}",
            tags=["Data - Table Level"],
            summary="Delete one or more records.",
            description="",
            )
async def delete_data(table_name: str,
                      filter: str = Header(None),
                      filterparam: str = Header(None),
                      current_user_role: bool = Depends(security.get_wirte_permission)):
    """
        Parameters

        - **table_name** (path): **Required** - Name of the table to perform operations on.
        - **filter** (header): Optional - SQL-like filter to limit the records to retrieve. ex: 'id=:qid and name=:qname'
        - **filterparam** (header): Optional - SQL-like parameter of *filter. ex: {'qid':3,'qname':'jack'}

    """
    log.logger.debug(
        'Access \'/_table/{table_name}\' : run in delete_data(), input data table_name: [%s]' % table_name)
    log.logger.debug('filter: [%s]' % filter)
    log.logger.debug('filterparam: [%s]' % filterparam)
    if not meta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    return delete.delete_table(table_name, filter, filterparam)

@api.get(prefix+"/_table/{table_name}/{id}",
         tags=["Data - Row Level"],
         summary="Retrieve one record by identifier.",
         description="",
         )
async def get_data_by_id(table_name: str, id: str,
                         fieldlist: str = Header('*'),
                         idfield: str = Header(None),
                         current_user: security.User = Depends(security.get_current_active_user)):
    """
        Parameters

        - **table_name** (path): **Required** - Name of the table to perform operations on.
        - **id** (path): **Required** - The id value of identifier
        - **fieldlist** (header): Optional - Comma-delimited list of properties to be returned for each resource, "*" returns all properties. ex: 'id,name'
        - **idfield** (header): Optional - Comma-delimited list of the fields used as identifiers. ex: 'id'
    """
    log.logger.debug(
        'Access \'/_table/{table_name}/{id}\' : run in get_data_by_id(), input data table_name: [%s]' % table_name)
    log.logger.debug('fieldlist: [%s]' % fieldlist)
    log.logger.debug('idfield: [%s]' % idfield)
    if not meta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    return query.query_table_byid(table_name,id,fieldlist,idfield)


@api.post(prefix+"/_table/{table_name}/querybyid",
          tags=["Data - Row Level"],
          summary="Retrieve one record by identifier.",
          description="",
          )
async def query_data_by_id(table_name: str, tablequerybyid:apimodel.TableQueryByIdBody,
                           current_user: security.User = Depends(security.get_current_active_user)):

    """
        Parameters

        - **table_name** (path): **Required** - Name of the table to perform operations on.
        - **request body: Required**
        ```
            {
            "fieldlist": "string",  -- Optional - Comma-delimited list of properties to be returned for each resource, "*" returns all properties. ex: 'id,name'
            "idfield": "string",  -- Optional - Comma-delimited list of the fields used as identifiers. ex: 'id'
            "id": "string"  -- **Required** - The id value of identifier
            }
        ```
        - **Note:** The param name in filter and filterparam **MUST NOT** equal the fieldname !
        - ex: 'id=:id' filter and  {'id':3} in filterparam will is **NOT PERMITTED** !
    """

    log.logger.debug(
        'Access \'/_table/{table_name}/querybyid\' : run in query_data_by_id(), input data table_name: [%s]' % table_name)
    log.logger.debug('body: [%s]' % tablequerybyid)
    if not meta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    return query.query_table_byid(table_name,tablequerybyid.id,tablequerybyid.fieldlist,tablequerybyid.idfield)

@api.put(prefix+"/_table/{table_name}/{id}",
         tags=["Data - Row Level"],
         summary="Replace the content of one record by identifier.",
         description="",
         )
async def put_data_by_id(table_name: str, id: str,
                         tableputbyid: apimodel.TablePutByIdBody,
                         current_user_role: bool = Depends(security.get_wirte_permission)):

    """
        Parameters

        - **table_name** (path): **Required** - Name of the table to perform operations on.
        - **id** (path): **Required** - The id value of identifier
        - **request body: Required**
        ```
            {
            "fieldvalue": "string"  -- Optional - Dict or jason formated fieldname-fieldvalue pair. ex: '[{'name':'jack','phone':'55789'}]'
            "idfield": "string",  -- Optional - Comma-delimited list of the fields used as identifiers. ex: 'id'
            }
        ```
        - **Note:** The param name in filter and filterparam **MUST NOT** equal the fieldname !
        - ex: 'id=:id' filter and  {'id':3} in filterparam will is **NOT PERMITTED** !
    """
    log.logger.debug(
        'Access \'/_table/{table_name}/{id}\' : run in put_data_by_id(), input data table_name: [%s]' % table_name)
    log.logger.debug('body: [%s]' % tableputbyid)
    if not meta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    return update.put_table_by_id(table_name, tableputbyid.idfield, id, tableputbyid.fieldvalue)

@api.delete(prefix+"/_table/{table_name}/{id}",
            tags=["Data - Row Level"],
            summary="Delete one record by identifier.",
            description="",
            )
async def delete_data_by_id(table_name: str, id: str,
                            idfield: str = Header(None, max_length=200),
                            current_user_role: bool = Depends(security.get_wirte_permission)):

    """
        Parameters

        - **table_name** (path): **Required** - Name of the table to perform operations on.
        - **id** (path): **Required** - The id value of identifier
        - **idfield** (header): Optional - Comma-delimited list of the fields used as identifiers. ex: 'id'
    """
    log.logger.debug(
        'Access \'/_table/{table_name}/{id}\' : run in delete_data_by_id(), input data table_name: [%s]' % table_name)
    log.logger.debug('id: [%s]' % id)
    log.logger.debug('idfield: [%s]' % idfield)
    if not meta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    return delete.delete_table_by_id(table_name, idfield, id)

@api.get("/sys/reloadmeta",
         tags=["System"],
         summary="Reload the DbSchemaResources.",
         description="",
         )
async def reload_meta(SecuretKey: str = Header(..., min_length=5),
                      current_user_role: bool = Depends(security.get_super_permission)):

    """
        Please use 'Confirm' as SecuretKey to confirm the operation

        - **SecuretKey** (header): **Required** - use 'Confirm' as the value.
    """
    log.logger.debug(
        'Access \'/sys/reloadmeta\' : run in reload_meta(), input data: [%s]' % str)
    if SecuretKey == 'Confirm':
        meta.DBMeta().load_activemeta()
        return {
        "Reload_Meta":'Sucessful'
        }
    else:
        return {
            "Reload_Meta": 'Operation Aborted'
        }

