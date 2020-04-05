# dbAPI

API in python dev with fastapi

uvicorn main:app --host 0.0.0.0 --port 3000 --reload --workers 2

gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:api -b 0.0.0.0:8890

/opt/pyAPI/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:api -b 0.0.0.0:8890