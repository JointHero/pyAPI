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
    'log_level' : '#pyapi_app_log_level#'
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
    'dialect' : '#pyapi_db_dialect#',
    'drivername': '#pyapi_db_drivername#',
    'host' : '#pyapi_db_host#',
    'port' : '#pyapi_db_port#',
    'dbname' : '#pyapi_db_dbname#',
    'username' : '#pyapi_db_username#',
    'password' : '#pyapi_db_password#',
    'dburi': '#pyapi_db_dburi#',
    'gendburi': #pyapi_db_gendburi#,
    'pool_size' : 20,
    'max_overflow' : 5,
    'limit_upset': #pyapi_db_limit_upset#,
    'default_limit': #pyapi_db_default_limit#,
    'default_offset': 0,
    'pool_use_lifo': #pyapi_db_pool_use_lifo#,
    'pool_pre_ping': #pyapi_db_pool_pre_ping#,
    'pool_recycle': #pyapi_db_pool_recycle#
}

#dburi = 'mysql+pymysql://root:passw0rd@192.168.10.15:23306/acmondb'
