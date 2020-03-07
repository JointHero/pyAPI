#!/usr/bin/env python
import os

app_config = {
    'name' : 'pyAPI',
    'version' : 'v1.01',
    'description' : 'Powered by Zino',
    'prefix' : '/api/v2',
    'metafile' : 'metadata.json',
    'param_prefix' : 'up_b_',
    'forcegenmeta' : True,
    'log_level' : 'DEBUG'
}
app_backend_cors_origins = os.getenv(
    "BACKEND_CORS_ORIGINS"
)
app_security = {
    'SECRET_KEY' : '47051d5e3bafcfcba3c80d6d1119a7adf78d2967a8972b00af1ea231ca61f589',
    'ALGORITHM' : 'HS256',
    'ACCESS_TOKEN_EXPIRE_MINUTES' : 30
}
db_config = {
    'dialect' : 'clickhouse',
    'drivername': 'clickhouse',
    'host' : '192.168.10.12',
    'port' : '28123',
    'dbname' : 'test',
    'username' : 'default',
    'password' : 'passw0rd',
    'dburi': 'clickhouse://default:passw0rd@192.168.10.12:28123/test',
    'gendburi': True,
    'pool_size' : 20,
    'max_overflow' : 5,
    'limit_upset': 2000,
    'default_limit': 20,
    'default_offset': 0,
    'pool_use_lifo': True,
    'pool_pre_ping': True,
    'pool_recycle': 3600
}

#dburi = 'mysql+pymysql://root:passw0rd@192.168.10.15:23306/acmondb'
