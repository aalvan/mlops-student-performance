# mlops-student-performance

# Docker network

```
docker network create shared_network
```

# MLflow

```
docker-compose --env-file mlflow.env -f mlflow.docker-compose.yml up --build

```

# Airflow
```
docker-compose -f airflow.docker-compose.yaml up airflow-init

docker-compose -f airflow.docker-compose.yaml up --build

```

# Web Service

```
docker-compose -f web-service.docker-compose.yml up --build
```

# Monitoring

```
docker-compose -f elk.docker-compose.yml up setup
docker-compose -f elk.docker-compose.yml up

```