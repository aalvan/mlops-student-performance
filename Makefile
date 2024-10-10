# Makefile for MLOps Project

# Default target
.DEFAULT_GOAL := help

# Help command
help:
	@echo "Makefile commands:"
	@echo "  make install            Install dependencies and project as a module"
	@echo "  make start              Start all services using Docker (MLflow, Airflow, Web Service, and ELK)"
	@echo "  make mlflow             Start MLflow service"
	@echo "  make airflow            Start Airflow scheduler, web server, and trigger a DAG"
	@echo "  make airflow-dag-trigger Trigger a specific Airflow DAG and monitor its status"
	@echo "  make web_service        Start the Web Service"
	@echo "  make elk                Start the ELK stack"
	
install:
	@echo "Updating pip..."
	pip install --upgrade pip
	@echo "Installing or updating pipenv..."
	pip install --upgrade pipenv
	@echo "Installing project dependencies..."
	pipenv install
	@echo "Installing the package in editable mode..."
	pipenv install --editable .
	@echo "All dependencies have been installed and updated."

setup-services:
	@echo "Creating shared Docker network if it doesn't exist..."
	docker network create shared_network || true  # Ignore error if the network exists
	@echo "Setting up ELK stack..."
	docker-compose -f src/monitoring/elk.docker-compose.yml up setup
	@echo "Creating .env file with AIRFLOW_UID..."
	echo "AIRFLOW_UID=$$(id -u)" > src/airflow/.env  # Save the .env file in the Airflow directory
	@echo "Initializing Airflow..."
	cd src/airflow && docker-compose -f airflow.docker-compose.yaml up airflow-init
	@echo "Airflow setup completed."

start-services: mlflow airflow airflow-dag-trigger web_service elk

mlflow:
	docker-compose --env-file mlflow.env -f mlflow.docker-compose.yml up -d --build

airflow:
	cd src/airflow && docker-compose -f airflow.docker-compose.yaml up -d --build
	sleep 60

airflow-dag-trigger:
	@echo "Triggering DAG..."
	DAG_ID="student_performance"; \
	AIRFLOW_URL="http://localhost:8080/api/v1/dags/$$DAG_ID/dagRuns"; \
	response=$$(curl -s -X POST \
		-u "airflow:airflow" \
		-H "Content-Type: application/json" \
		-d '{"conf": {}}' \
		"$$AIRFLOW_URL"); \
	echo "Response: $$response"; \
	run_id=$$(echo $$response | jq -r '.dag_run_id'); \
	echo "Run ID: $$run_id"; \
	STATUS_URL="http://localhost:8080/api/v1/dags/$$DAG_ID/dagRuns/$$run_id"; \
	echo "Checking status of the DAG run..."; \
	while true; do \
		status_response=$$(curl -s -X GET -u "airflow:airflow" "$$STATUS_URL"); \
		state=$$(echo $$status_response | jq -r '.state'); \
		echo "Current state: $$state"; \
		if [ "$$state" = "success" ] || [ "$$state" = "failed" ] || [ "$$state" = "skipped" ]; then \
			echo "DAG run finished with state: $$state"; \
			break; \
		fi; \
		sleep 5; \
	done
	
web_service:
	docker-compose -f src/web_service/web-service.docker-compose.yml up -d --build

elk:
	docker-compose -f  src/monitoring/elk.docker-compose.yml up -d --build

stop-services:
	@echo "Stopping all Docker containers..."
	docker-compose --env-file mlflow.env -f mlflow.docker-compose.yml down
	cd src/airflow && docker-compose -f airflow.docker-compose.yaml down
	docker-compose -f src/web_service/web-service.docker-compose.yml down
	docker-compose -f src/monitoring/elk.docker-compose.yml down
	@echo "All containers have been stopped."
