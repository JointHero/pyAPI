# pyAPI
RDBMS API Server base on FastAPI

uvicorn main:api --host 0.0.0.0 --port 3000 --reload --workers 2

gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:api -b 0.0.0.0:8890