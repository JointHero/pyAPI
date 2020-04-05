#!/bin/bash
export PYAPI_application_app_force_generate_meta=${PYAPI_application_app_force_generate_meta:-'true'}
export PYAPI_application_app_log_level=${PYAPI_application_app_log_level:-'INFO'}
export PYAPI_application_app_user_func=${PYAPI_application_app_user_func:-'true'}
export PYAPI_application_app_exception_detail=${PYAPI_application_app_exception_detail:-'true'}
export PYAPI_schema_schema_cache_enabled=${PYAPI_schema_schema_cache_enabled:-'true'}
export PYAPI_schema_schema_fetch_all_table=${PYAPI_schema_schema_fetch_all_table:-'true'}
export PYAPI_schema_schema_fetch_tables=${PYAPI_schema_schema_fetch_tables:-'mytable'}
export PYAPI_query_query_limit_upset=${PYAPI_query_query_limit_upset:-'2000'}
export PYAPI_query_query_default_limit=${PYAPI_query_query_default_limit:-'20'}
export PYAPI_query_query_default_offset=${PYAPI_query_query_default_offset:-'0'}
export PYAPI_security_access_token_expire_minutes=${PYAPI_security_access_token_expire_minutes:-'30'}
export PYAPI_database_db_gendburi=${PYAPI_database_db_gendburi:-'true'}
export PYAPI_database_db_dialect=${PYAPI_database_db_dialect:-'mysql'}
export PYAPI_database_db_drivername=${PYAPI_database_db_drivername:-'mysql+pymysql'}
export PYAPI_database_db_host=${PYAPI_database_db_host:-'server'}
export PYAPI_database_db_port=${PYAPI_database_db_port:-'3306'}
export PYAPI_database_db_name=${PYAPI_database_db_name:-'db'}
export PYAPI_database_db_schema=${PYAPI_database_db_schema:-'schema'}
export PYAPI_database_db_use_schema=${PYAPI_database_db_use_schema:-'true'}
export PYAPI_database_db_username=${PYAPI_database_db_username:-'root'}
export PYAPI_database_db_password=${PYAPI_database_db_password:-'password'}
export PYAPI_database_db_uri=${PYAPI_database_db_uri:-'mysql+pymysql://root:password@server:3306/db'}
export PYAPI_database_db_exclude_tablespaces=${PYAPI_database_db_exclude_tablespaces:-'SYSTEM'}
export PYAPI_connection_con_pool_size=${PYAPI_connection_con_pool_size:-'20'}
export PYAPI_connection_con_max_overflow=${PYAPI_connection_con_max_overflow:-'5'}
export PYAPI_connection_con_pool_recycle=${PYAPI_connection_con_pool_recycle:-'3600'}
export pyapi_gunicorn_ip=${pyapi_gunicorn_ip:-'0.0.0.0'}
export pyapi_gunicorn_port=${pyapi_gunicorn_port:-'8890'}
export pyapi_app_protocal=${pyapi_app_protocal:-'http'}
export pyapi_gunicorn_workers=${pyapi_gunicorn_workers:-2}
export pyapi_gunicorn_timeout=${pyapi_gunicorn_timeout:-60}
export pyapi_gunicorn_threads=${pyapi_gunicorn_threads:-2}
export ORACLE_HOME=/opt/instantclient
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME
cp /opt/pyAPI/config/config_template.yml /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_application_app_force_generate_meta#/${PYAPI_application_app_force_generate_meta}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_application_app_log_level#/${PYAPI_application_app_log_level}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_application_app_user_func#/${PYAPI_application_app_user_func}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_application_app_exception_detail#/${PYAPI_application_app_exception_detail}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_schema_schema_cache_enabled#/${PYAPI_schema_schema_cache_enabled}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_schema_schema_fetch_all_table#/${PYAPI_schema_schema_fetch_all_table}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_schema_schema_fetch_tables#/${PYAPI_schema_schema_fetch_tables}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_query_query_limit_upset#/${PYAPI_query_query_limit_upset}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_query_query_default_limit#/${PYAPI_query_query_default_limit}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_query_query_default_offset#/${PYAPI_query_query_default_offset}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_security_access_token_expire_minutes#/${PYAPI_security_access_token_expire_minutes}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_database_db_gendburi#/${PYAPI_database_db_gendburi}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_database_db_dialect#/${PYAPI_database_db_dialect}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_database_db_drivername#/${PYAPI_database_db_drivername}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_database_db_host#/${PYAPI_database_db_host}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_database_db_port#/${PYAPI_database_db_port}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_database_db_name#/${PYAPI_database_db_name}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_database_db_schema#/${PYAPI_database_db_schema}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_database_db_use_schema#/${PYAPI_database_db_use_schema}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_database_db_username#/${PYAPI_database_db_username}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_database_db_password#/${PYAPI_database_db_password}/g" /opt/pyAPI/config/config.yml
sed -i "s~#PYAPI_database_db_uri#~${PYAPI_database_db_uri}~g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_database_db_exclude_tablespaces#/${PYAPI_database_db_exclude_tablespaces}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_connection_con_pool_size#/${PYAPI_connection_con_pool_size}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_connection_con_max_overflow#/${PYAPI_connection_con_max_overflow}/g" /opt/pyAPI/config/config.yml
sed -i "s/#PYAPI_connection_con_pool_recycle#/${PYAPI_connection_con_pool_recycle}/g" /opt/pyAPI/config/config.yml
cp /opt/pyAPI/config/gunicorn_template.py /opt/pyAPI/config/gunicorn.py
sed -i "s/#pyapi_gunicorn_ip#/${pyapi_gunicorn_ip}/g" /opt/pyAPI/config/gunicorn.py
sed -i "s/#pyapi_gunicorn_port#/${pyapi_gunicorn_port}/g" /opt/pyAPI/config/gunicorn.py
sed -i "s/#pyapi_gunicorn_workers#/${pyapi_gunicorn_workers}/g" /opt/pyAPI/config/gunicorn.py
sed -i "s/#pyapi_gunicorn_timeout#/${pyapi_gunicorn_timeout}/g" /opt/pyAPI/config/gunicorn.py
sed -i "s/#pyapi_gunicorn_threads#/${pyapi_gunicorn_threads}/g" /opt/pyAPI/config/gunicorn.py
if [ "a$pyapi_app_protocal" == "ahttp" ]; then
    sed -i "s/keyfile/#keyfile/g" /opt/pyAPI/config/gunicorn.py
    sed -i "s/certfile/#certfile/g" /opt/pyAPI/config/gunicorn.py
fi
cd /opt/pyAPI && \
/opt/pyAPI/venv/bin/gunicorn -c /opt/pyAPI/config/gunicorn.py main:app 