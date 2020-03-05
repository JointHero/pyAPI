#!/usr/bin/env python


from pydantic import BaseModel
from config import config

class TableQueryBody(BaseModel):
    fieldlist: str = '*'
    filter: str = None
    filterparam: str = None
    limit: int = config.db_config['default_limit']
    offset: int = config.db_config['default_offset']
    order: str = None
    group: str = None
    count_only: bool = False
    include_count: bool = False

class TableQueryByIdBody(BaseModel):
    fieldlist: str = '*'
    idfield: str = None
    id: str = None

class TablePostBody(BaseModel):
    fieldvalue: str = None
    idfield: str = None

class TablePutByIdBody(BaseModel):
    fieldvalue: str = None
    idfield: str = None

class TablePutBody(BaseModel):
    filter: str = None
    filterparam: str = None
    fieldvalue: str = None
