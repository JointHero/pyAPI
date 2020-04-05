#!/usr/bin/env python
# -*- coding: utf-8 -*-


import ast
import re
from urllib import parse

import simplejson as json
from sqlalchemy.engine.url import URL

from config import config


def is_dict(dictstr):
    if isinstance(dictstr,dict):
        return True
    else:
        try:
            ast.literal_eval(dictstr)
        except ValueError:
            return False
        return True


def to_dict(dictstr):
    if isinstance(dictstr, dict):
        return dictstr
    elif is_dict(dictstr):
        return ast.literal_eval(dictstr)
    else:
        return None

def is_json(jsonstr):
    try:
        json.loads(jsonstr)
    except ValueError:
        return False
    return True


def to_json(jsonstr):
    if is_json(jsonstr):
        return json.loads(jsonstr)
    else:
        return None

def is_list(str):
    try:
        re.split(r'[\s\,\;]+', str)
    except TypeError:
        return False
    return True

def to_list(str):
    if is_list(str):
        return re.split(r'[\s\,\;]+', str)
    else:
        return  [str]

def is_fvcol(str):
    try:
        ast.literal_eval(str)
    except SyntaxError:
        return False
    return True

def to_fvcol(str):
    if is_fvcol(str):
        return ast.literal_eval(str)
    else:
        return None

def uappend(str):
    return config.Config().application['app_param_prefix']+'{}'.format(str)

def uappendlist(slist):
    return list(map(uappend,slist))

def gen_dburi():
    cfg = config.Config()
    db = {'drivername': cfg.database['db_drivername'],
          'username': cfg.database['db_username'],
          'password': parse.unquote_plus(cfg.database['db_password']),
          'host': cfg.database['db_host'],
          'port': cfg.database['db_port'],
          'database':cfg.database['db_name']
          }
    return URL(**db)

if __name__ == '__main__':
    '''
    print(uappendlist(['id', 'name', 'phone']))
    test = '{"id":3,"name":"sdf"}'
    testl = '{"id":3,"name":"sdf","phone":"234243"},{"id":3,"name":"sdf","phone":"234243"},{"id":3,"name":"sdf","phone":"234243"}'
    teddd = '{\'name\': \'zhangjun\',\'phone\':\'241124\'}'
    print(to_fvcol(teddd))
    print(to_fvcol(testl))
    pstr = [{'name':'zhjjj'},{'id':12},{'phone':'12345'}]
    fstr = 'name=:name and id = :id or phone =  :phone '
    print(str(gen_dburi()))
    '''
    print(is_dict("{'aa','ddd'}"))
    print(isinstance("{'id':3,'name':'sdf'}",dict))


