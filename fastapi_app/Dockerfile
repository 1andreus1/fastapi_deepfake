FROM python:3.10

COPY requirements_fastapi.txt .

RUN pip install -r requirements_fastapi.txt

RUN mkdir -p /deep_fake/fastapi_app

WORKDIR /deep_fake/fastapi_app

COPY . .

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000