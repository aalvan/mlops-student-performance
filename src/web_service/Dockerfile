FROM python:3.12-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["predict.py", "./"]

EXPOSE 8000

ENTRYPOINT [ "uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "8000"]
