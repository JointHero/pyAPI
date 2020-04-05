#!/usr/bin/env python

import requests
import simplejson as json
import urllib3

from config import config
from util import log

urllib3.disable_warnings()

'''config'''
cfg = config.Config()

'''logging'''
log = log.Logger(level=cfg.application['app_log_level'])


host = 'http://192.168.10.19:48890/'
apiprefix = 'api/v2'

#################################################
# Access api root
#################################################
log.logger.info('= '*50)
log.logger.info('Access api root: ')
resp = requests.get(host, verify=False)
log.logger.info('* ' * 50)
log.logger.info('Status Code: [ %s ]' % resp.status_code)
log.logger.info('Response: \n %s ' % json.dumps(resp.json(),
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))
#################################################
# Get access tocken
#################################################
log.logger.info('= '*50)
log.logger.info('Get access tocken: ')
uri = host + apiprefix +'/token'
log.logger.info('POST uri: [ %s ]' % uri)
body = {'username':'admin','password':'admin'}
log.logger.info('Post body: \n %s ' % json.dumps(body,
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))
resp = requests.post(uri,
                     data=body,  # 直接作为body提交
                     headers={'Content-Type':'application/x-www-form-urlencoded','accept': 'application/json'},
                     verify=False)
log.logger.info('Response: \n %s ' % json.dumps(resp.json(),
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))

tokenstr = None
if resp.status_code == 200:
    tokenstr = resp.json()['token_type'].capitalize() + ' ' + resp.json()['access_token']
    log.logger.info('Token: \n %s ' % tokenstr)

#################################################
# Get user info
#################################################
log.logger.info('= '*50)
log.logger.info('Get user info: ')
uri = host + apiprefix +'/users/me/'
log.logger.info('GET uri : [ %s ]' % uri)
resp = requests.get(uri,
                    headers={'Authorization':tokenstr,'accept': 'application/json'},
                    verify=False)
log.logger.info('* ' * 50)
log.logger.info('Status Code: [ %s ]' % resp.status_code)
log.logger.info('Response: \n %s ' % json.dumps(resp.json(),
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))

#################################################
# Get schema list
#################################################
log.logger.info('= '*50)
log.logger.info('Get schema list: ')
uri = host + apiprefix +'/_schema'
log.logger.info('GET uri : [ %s ]' % uri)
resp = requests.get(uri,
                    headers={'Authorization':tokenstr,'accept': 'application/json'},
                    verify=False)
log.logger.info('* ' * 50)
log.logger.info('Status Code: [ %s ]' % resp.status_code)
log.logger.info('Response: \n %s ' % json.dumps(resp.json(),
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))

#################################################
# Get schema list
#################################################
log.logger.info('= '*50)
log.logger.info('Get schema [test] : ')
tablename = 'test'
uri = host + apiprefix +'/_schema/' + tablename
log.logger.info('GET uri : [ %s ]' % uri)
resp = requests.get(uri,
                    headers={'Authorization':tokenstr,'accept': 'application/json'},
                    verify=False)
log.logger.info('* ' * 50)
log.logger.info('Status Code: [ %s ]' % resp.status_code)
log.logger.info('Response: \n %s ' % json.dumps(resp.json(),
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))

#################################################
# Query table
#################################################
log.logger.info('= '*50)
log.logger.info('Query table [test] : ')
tablename = 'test'
fieldlist = '*'
filter=None
filterparam=None
limit='10'
offset='0'
order=None
group=None
count_only='False'
include_count='False'
uri = host + apiprefix +'/_table/' + tablename
log.logger.info('GET uri : [ %s ]' % uri)
resp = requests.get(uri,
                    headers={'Authorization':tokenstr,
                             'fieldlist':fieldlist,
                             'filter':filter,
                             'filterparam':filterparam,
                             'limit':limit,
                             'offset':offset,
                             'order':order,
                             'group':group,
                             'count_only':count_only,
                             'include_count':include_count,
                             'accept': 'application/json'},
                    verify=False)
log.logger.info('* ' * 50)
log.logger.info('Status Code: [ %s ]' % resp.status_code)
log.logger.info('Response: \n %s ' % json.dumps(resp.json(),
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))

#################################################
# Query table by id
#################################################
log.logger.info('= '*50)
log.logger.info('Query table by id [test] : ')
tablename = 'test'
fieldlist = '*'
id='66'
idfield='id'
uri = host + apiprefix +'/_table/' + tablename + '/' + id
log.logger.info('GET uri : [ %s ]' % uri)
resp = requests.get(uri,
                    headers={'Authorization':tokenstr,
                             'fieldlist':fieldlist,
                             'idfield':idfield,
                             'accept': 'application/json'},
                    verify=False)
log.logger.info('* ' * 50)
log.logger.info('Status Code: [ %s ]' % resp.status_code)
log.logger.info('Response: \n %s ' % json.dumps(resp.json(),
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))

#################################################
# POST Query table
#################################################
log.logger.info('= '*50)
log.logger.info('POST Query table [test] : ')
tablename = 'test'

body = {"fieldlist": "*",
  "filter": "id>:qid",
  "filterparam": "{'qid':6}",
  "limit": 5,
  "offset": 0,
#  "order": "id desc",
#  "group": "name",
  "count_only": False,
  "include_count": True
}

log.logger.info('Post body: \n %s ' % json.dumps(body,
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))
uri = host + apiprefix +'/_table/' + tablename + '/query'
log.logger.info('POST uri : [ %s ]' % uri)
resp = requests.post(uri,
                     data=json.dumps(body),   # 序列化json字符串后作为body提交
                     headers={'Authorization':tokenstr,
                              'Content-Type':'application/json',
                              'accept': 'application/json'},
                     verify=False)
log.logger.info('* ' * 50)
log.logger.info('Status Code: [ %s ]' % resp.status_code)
log.logger.info('Response: \n %s ' % json.dumps(resp.json(),
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))

#################################################
# POST Query table by id
#################################################
log.logger.info('= '*50)
log.logger.info('POST Query table by id [test] : ')
tablename = 'test'

body = {
  "fieldlist": "*",
  "idfield": "id",
  "id": "66"
}

log.logger.info('Post body: \n %s ' % json.dumps(body,
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))
uri = host + apiprefix +'/_table/' + tablename + '/querybyid'
log.logger.info('POST uri : [ %s ]' % uri)
resp = requests.post(uri,
                     data=json.dumps(body),   # 序列化json字符串后作为body提交
                     headers={'Authorization':tokenstr,
                              'Content-Type':'application/json',
                              'accept': 'application/json'},
                     verify=False)
log.logger.info('* ' * 50)
log.logger.info('Status Code: [ %s ]' % resp.status_code)
log.logger.info('Response: \n %s ' % json.dumps(resp.json(),
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))

#################################################
# POST table
#################################################
log.logger.info('= '*50)
log.logger.info('POST table [test] : ')
tablename = 'test'

body = {
  "fieldvalue": "{'name':'ntestname','phone':'phonnum-123'}",
  "idfield": "id"
}

log.logger.info('Post body: \n %s ' % json.dumps(body,
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))
uri = host + apiprefix +'/_table/' + tablename
log.logger.info('POST uri : [ %s ]' % uri)
resp = requests.post(uri,
                     data=json.dumps(body),   # 序列化json字符串后作为body提交
                     headers={'Authorization':tokenstr,
                              'Content-Type':'application/json',
                              'accept': 'application/json'},
                     verify=False)
log.logger.info('* ' * 50)
log.logger.info('Status Code: [ %s ]' % resp.status_code)
log.logger.info('Response: \n %s ' % json.dumps(resp.json(),
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))

insertid=resp.json()['insert_row_id']
log.logger.info('Insert ID: \n %s ' % insertid)

#################################################
# PUT table
#################################################
log.logger.info('= '*50)
log.logger.info('PUT table [test] : ')
tablename = 'test'

body = {
  "filter": "id=:pid",
  "filterparam": "{'pid':"+str(insertid)+"}",
  "fieldvalue": "{'name':'anewname','phone':'54321'}"
}

log.logger.info('Put body: \n %s ' % json.dumps(body,
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))
uri = host + apiprefix +'/_table/' + tablename
log.logger.info('PUT uri : [ %s ]' % uri)
resp = requests.put(uri,
                     data=json.dumps(body),   # 序列化json字符串后作为body提交
                     headers={'Authorization':tokenstr,
                              'Content-Type':'application/json',
                              'accept': 'application/json'},
                     verify=False)
log.logger.info('* ' * 50)
log.logger.info('Status Code: [ %s ]' % resp.status_code)
log.logger.info('Response: \n %s ' % json.dumps(resp.json(),
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))

#################################################
# DELETE table
#################################################
log.logger.info('= '*50)
log.logger.info('DELETE table [test] : ')
tablename = 'test'
filter = "id=:delid"
filterparam = "{'delid':"+str(insertid)+"}"
uri = host + apiprefix +'/_table/' + tablename
log.logger.info('DELETE uri : [ %s ]' % uri)
resp = requests.delete(uri,
                     headers={'Authorization':tokenstr,
                              'filter':filter,
                              'filterparam':filterparam,
                              'Content-Type':'application/json',
                              'accept': 'application/json'},
                     verify=False)
log.logger.info('* ' * 50)
log.logger.info('Status Code: [ %s ]' % resp.status_code)
log.logger.info('Response: \n %s ' % json.dumps(resp.json(),
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))

#################################################
# POST table
#################################################
log.logger.info('= '*50)
log.logger.info('POST table [test] : ')
tablename = 'test'

body = {
  "fieldvalue": "{'name':'ntestname','phone':'phonnum-123'}",
  "idfield": "id"
}

log.logger.info('Post body: \n %s ' % json.dumps(body,
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))
uri = host + apiprefix +'/_table/' + tablename
log.logger.info('POST uri : [ %s ]' % uri)
resp = requests.post(uri,
                     data=json.dumps(body),   # 序列化json字符串后作为body提交
                     headers={'Authorization':tokenstr,
                              'Content-Type':'application/json',
                              'accept': 'application/json'},
                     verify=False)
log.logger.info('* ' * 50)
log.logger.info('Status Code: [ %s ]' % resp.status_code)
log.logger.info('Response: \n %s ' % json.dumps(resp.json(),
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))

insertid=resp.json()['insert_row_id']
log.logger.info('Insert ID: \n %s ' % insertid)


#################################################
# PUT table by id
#################################################
log.logger.info('= '*50)
log.logger.info('PUT table by id [test] : ')
tablename = 'test'
id = insertid
body = {
  "idfield": "id",
  "fieldvalue": "{'name':'anewname','phone':'54321'}"
}

log.logger.info('Put body: \n %s ' % json.dumps(body,
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))
uri = host + apiprefix +'/_table/' + tablename + "/" + str(id)
log.logger.info('PUT uri : [ %s ]' % uri)
resp = requests.put(uri,
                     data=json.dumps(body),   # 序列化json字符串后作为body提交
                     headers={'Authorization':tokenstr,
                              'Content-Type':'application/json',
                              'accept': 'application/json'},
                     verify=False)
log.logger.info('* ' * 50)
log.logger.info('Status Code: [ %s ]' % resp.status_code)
log.logger.info('Response: \n %s ' % json.dumps(resp.json(),
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))

#################################################
# DELETE table by id
#################################################
log.logger.info('= '*50)
log.logger.info('DELETE table by id [test] : ')
tablename = 'test'
id = insertid
idfiled = "id"
uri = host + apiprefix +'/_table/' + tablename + "/" + str(id)
log.logger.info('DELETE uri : [ %s ]' % uri)
resp = requests.delete(uri,
                     headers={'Authorization':tokenstr,
                              'idfiled':idfiled,
                              'Content-Type':'application/json',
                              'accept': 'application/json'},
                     verify=False)
log.logger.info('* ' * 50)
log.logger.info('Status Code: [ %s ]' % resp.status_code)
log.logger.info('Response: \n %s ' % json.dumps(resp.json(),
                                                separators=(',', ':'),
                                                sort_keys=False,
                                                indent=4 * ' ',
                                                encoding='utf-8'))

