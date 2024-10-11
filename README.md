![mlops-diagram](https://github.com/user-attachments/assets/56d235aa-6598-4804-81e9-f495b3afd227)

# Student Performance Prediction with MLOps
[![CI/CD Workflow](https://github.com/aalvan/mlops-student-performance/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/aalvan/mlops-student-performance/actions/workflows/ci-cd.yml)

## Project Overview

This project aims to build an end-to-end MLOps pipeline that predicts student performance based on a variety of academic, socio-economic, and behavioral factors. The model is designed to help educational institutions proactively identify students at risk of underperformance, enabling early interventions and personalized support strategies.

The project demonstrates the complete lifecycle of machine learning, from data collection and model development to deployment, monitoring, and continuous integration. By leveraging MLOps principles, we ensure that the solution is scalable, reproducible, and maintainable.

**Note**:
The "Student Performance Factors" dataset used in this project is a synthetic dataset generated for educational and analytical purposes. The data is not sourced from any real-world institutions but is created to simulate realistic scenarios for analyzing student performance factors. As such, the results and predictions should not be used in real-world decision-making. Care should be taken when interpreting the outcomes, as the model's performance is based solely on this synthetic dataset and may not generalize to different or actual student populations.

--------

## Table of Contents

1. [Project Overview](#project-overview)
2. [Docker Network](#docker-network)  
   2.1. [Creating the Docker Network](#creating-the-docker-network)
3. [MLflow: Experiment Tracking and Model Registration](#mlflow-experiment-tracking-and-model-registration)  
   3.1. [Starting MLflow](#starting-mlflow)  
   3.2. [Important Note](#important-note)
4. [Orchestration](#orchestration)  
   4.1. [Starting Airflow](#starting-airflow)  
       4.1.1. [Initialize the Airflow Database](#initialize-the-airflow-database)  
       4.1.2. [Start Airflow Services](#start-airflow-services)
5. [Web Service](#web-service)  
   5.1. [Running the Web Service](#running-the-web-service)  
6. [Monitoring Logs](#monitoring-logs)  
   6.1. [Setting Up the ELK Stack](#setting-up-the-elk-stack)  
       6.1.1. [Initialize the Services](#initialize-the-services)  
       6.1.2. [Start the ELK Stack](#start-the-elk-stack)  
   6.2. [Visualizing Logs](#visualizing-logs)
7. [GitHub Actions CI/CD](#github-actions-cicd)  
   7.1. [Workflow Overview](#workflow-overview)  
   7.2. [Workflow Configuration](#workflow-configuration)  
   7.3. [Getting Started](#getting-started)
8. [Installation](#installation)  
   8.1. [Prerequisites](#prerequisites)  
   8.2. [Steps](#steps)
9. [Makefile](#makefile)
   9.1. [Makefile Commands](#makefile-commands)  
   9.2. [Recommended Workflow](#recommended-workflow)  
   


## Docker Network

A shared Docker network is created to facilitate communication between the various services in the project. This ensures that the different containers can interact seamlessly with each other.

### Creating the Docker Network

To create the shared Docker network, run the following command:

```bash
docker network create shared_network
```

## MLflow: Experiment Tracking and Model Registration

MLflow is an open-source platform for managing the machine learning lifecycle. In this project, MLflow is utilized primarily for tracking experiments and registering models, enabling better organization and reproducibility of machine learning workflows.

### Starting MLflow

Before starting the other services, ensure that MLflow is up and running to guarantee proper functionality. Use the following command to start the MLflow service:

```bash
docker-compose --env-file mlflow.env -f mlflow.docker-compose.yml up --build
```
### Important Note

It is crucial to start the MLflow service before any other services (such as Airflow and the web service) to ensure that they can properly connect to and utilize MLflow’s tracking and model registration capabilities. Failing to do so may lead to connectivity issues and hinder the effectiveness of the machine learning lifecycle management in this project.

## Orchestration

Apache Airflow is an open-source platform to programmatically create, schedule, and monitor workflows. In this project, Airflow is used for orchestrating the machine learning workflows, ensuring that tasks are executed in the correct order and dependencies are managed effectively.

### Starting Airflow

To initialize and start the Airflow services, use the following commands:

1. **Initialize the Airflow Database**:
   These commands set up the necessary database for Airflow to manage its metadata and task states.

   ```bash
   echo -e "AIRFLOW_UID=$(id -u)" > .env
   docker-compose -f airflow.docker-compose.yaml up airflow-init
   ```
2. **Start Airflow Services**: After initializing, start the Airflow services with the following command:

    ```bash
    docker-compose -f airflow.docker-compose.yaml up --build
    ```
## Web Service

This project includes a web service that consists of two main components: an API built using FastAPI and a user interface created with Streamlit. The FastAPI backend handles model predictions and serves the machine learning model, while the Streamlit frontend provides an interactive interface for users to input data and visualize results.
### Running the Web Service

Both the FastAPI API and the Streamlit interface are containerized and can be run together using Docker Compose. The following command will build and start the services in Docker containers:
```
docker-compose -f web-service.docker-compose.yml up --build
```
**FastAPI URL**:  
Once the service is up, you can access the API documentation (Swagger UI) at:  
`http://localhost:8000/docs`

**Streamlit URL**:  
The Streamlit interface will be available at:  
`http://localhost:8501`

## Monitoring Logs

This project utilizes the **ELK Stack** (Elasticsearch, Logstash, and Kibana) for monitoring logs and visualizing system performance. The ELK stack provides powerful tools for searching, analyzing, and visualizing log data in real-time.

### Setting Up the ELK Stack

To set up the ELK stack, run the following command to initialize the services:

1. **Initialize the Services**:
   Run the following command to set up the necessary configurations and prepare the ELK stack for use:

   ```bash
   docker-compose -f elk.docker-compose.yml up setup
   ```
2. **Start the ELK Stack**: 
    Once the setup is complete, you can start the ELK stack with the following command:
    ```bash
    docker-compose -f elk.docker-compose.yml up
    ```
### Visualizing Logs

Logs can be visualized in Kibana while utilizing the Streamlit app. As users interact with the Streamlit interface, logs are generated and sent to the ELK stack for analysis and visualization. For visualizing logs connect to Kibana at `http://localhost:5601`.

## GitHub Actions CI/CD

This project utilizes **GitHub Actions** to automate the continuous integration and continuous deployment (CI/CD) processes. The CI/CD workflow is triggered by pushes to the main branch, as well as pull requests targeting the main branch. Additionally, it supports manual triggers for greater flexibility.

### Workflow Overview

The CI/CD workflow consists of the following steps:

1. **Checkout the Repository**: The workflow begins by checking out the code from the repository.
   
2. **Set Up Environment**: 
   - Sets up Docker Buildx for building Docker images.
   - Installs Python 3.12 using the `setup-python` action.
   - Installs Docker Compose.

3. **Install Dependencies**: Installs the necessary Python packages using Pipenv.

4. **Create Shared Network**: A Docker network named `shared_network` is created to allow communication between containers.

5. **Start Services**:
   - **MLflow Service**: The MLflow service is started using a Docker Compose file.
   - **Airflow Service**: The Airflow service is initialized and started, allowing for task orchestration.

6. **Trigger Airflow DAG**: The workflow triggers a specified Airflow DAG to execute tasks defined within it.

7. **Start Web Service**: The FastAPI web service is started using Docker Compose.

8. **Install FastAPI Dependencies**: Installs dependencies from the `Pipfile` for the FastAPI application.

9. **Run Tests**:
   - Runs a request test to ensure the web service is functioning as expected.
   - Executes unit tests for the FastAPI application using pytest.

10. **Stop Services**: Finally, the workflow stops all running Docker services to clean up resources.

### Workflow Configuration

The CI/CD workflows are defined in the `.github/workflows` directory of the repository. Each workflow file outlines the steps required for the automated processes, including:
- Triggering on specific events (e.g., push, pull requests, manual triggers).
- Specifying jobs to run (e.g., testing, building, deploying).
- Using environment variables and secrets for secure configuration.

### Getting Started

To set up GitHub Actions for your fork of this project, ensure that the necessary secrets and environment variables are configured in your repository settings. This setup will allow the CI/CD pipeline to run smoothly, automating the testing and deployment process whenever changes are made.

By using GitHub Actions, we ensure a robust, efficient, and automated workflow, enhancing the development experience and minimizing the risk of errors during deployments.

## Installation
> [!NOTE]
> This project was originally created on GitHub Codespaces using a 4-core 16GB RAM • 32GB machine. If you want to run the code easily, consider using GitHub Codespaces for a seamless experience.


### Prerequistes 
    - Python 3.12
    - Pipenv
    - Docker
### Steps
To simplify the installation and setup process, you can utilize the Makefile commands instead of manual steps. However, if you prefer to do it manually, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/aalvan/mlops-student-performance.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd mlops-student-performance
    ```

3. **Install dependencies using `pipenv`:**

    ```bash
    pipenv install
    ```

4. **Activate the Pipenv shell:**

    ```bash
    pipenv shell
    ```

5. **Install the project as a module using `setup.py`:**

    ```bash
    pipenv install --editable .
    ```

## Makefile

The Makefile automates project management tasks, including:

- **Installation**: Sets up Python dependencies and installs the project.
- **Service Management**: Starts and stops essential services like MLflow, Airflow, Web Service, and ELK.
- **Airflow DAG Handling**: Unpauses and triggers specific Airflow DAGs while monitoring their status.
- **Testing**: Runs unit tests using pytest.

### Makefile Commands

- **help**: Displays a list of available commands and their descriptions.
- **install**: Installs or updates project dependencies and sets up the project in editable mode.
- **setup-services**: Creates a Docker network and initializes the ELK stack and Airflow.
- **start-services**: Launches all services (MLflow, Airflow, Web Service, and ELK).
- **mlflow**: Starts the MLflow service using Docker.
- **airflow**: Starts the Airflow scheduler and web server and waits for them to be reachable.
- **airflow-dag-trigger**: Unpauses and triggers a specific Airflow DAG, monitoring its execution status.
- **web_service**: Starts the Web Service using Docker.
- **elk**: Starts the ELK stack using Docker.
- **test**: Runs unit tests for the Web Service using pytest.
- **stop-services**: Stops all running Docker containers associated with the project.

### Recommended Workflow

To run the commands correctly, follow this order:

1. **install**: Set up dependencies and project configuration.
2. **setup-services**: Initialize the Docker network and services.
3. **start-services**: Launch all necessary services.

> **Important Note**: Always run **start-services** before executing tests to ensure all necessary services are running.

After running these commands, the entire setup will be ready for use. 