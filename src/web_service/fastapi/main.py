import logging
import time
from typing import Callable

import logstash
import pandas as pd

from fastapi import FastAPI, HTTPException, Request, Response
from starlette.background import BackgroundTask

from models.features import Features

from sklearn.preprocessing import OrdinalEncoder, LabelEncoder

import mlflow
from mlflow import MlflowClient


host = "logstash"
logger = logging.getLogger("python-logstash-logger")
logger.setLevel(logging.INFO)
logger.addHandler(logstash.TCPLogstashHandler(host, 50000, version=1))

def log_info(log_data):
    logger.info("Log Data", extra={"@fields": log_data})

EXPERIMENT = 'student_performance'
TRACKING_SERVER_HOST = "mlflow_server"
mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")
mlflow.set_experiment(EXPERIMENT)
MLFLOW_TRACKING_URI = mlflow.get_tracking_uri()
print(MLFLOW_TRACKING_URI)

client = MlflowClient(MLFLOW_TRACKING_URI)

model_name = "student-performance-predictor"
model_alias = 'best'
model_version_info = client.get_model_version_by_alias(model_name, model_alias)
model_version = model_version_info.version
model_uri = f"models:/{model_name}/{model_version}"
RUN_ID = model_version_info.run_id

model = mlflow.pyfunc.load_model(model_uri)

def predict(features: Features):

    input_data = {
        "Hours_Studied": [features.hours_studied],
        "Attendance": [features.attendance],
        "Parental_Involvement": [features.parental_involvement.value],  # Use .value for enums
        "Access_to_Resources": [features.access_to_resources.value],
        "Extracurricular_Activities": [1 if features.extracurricular_activities else 0],
        "Sleep_Hours": [features.sleep_hours],
        "Previous_Scores": [features.previous_scores],
        "Motivation_Level": [features.motivation_level.value],
        "Internet_Access": [1 if features.internet_access else 0],
        "Tutoring_Sessions": [features.tutoring_sessions],
        "Family_Income": [features.family_income.value],
        "Teacher_Quality": [features.teacher_quality.value],
        "School_Type": [features.school_type.value],
        "Peer_Influence": [features.peer_influence.value],
        "Physical_Activity": [features.physical_activity],
        "Learning_Disabilities": [1 if features.learning_disabilities else 0],
        "Parental_Education_Level": [features.parental_education_level.value],
        "Distance_from_Home": [features.distance_from_home.value],
        "Gender": [features.gender.value],
    }

    #input_data = pd.DataFrame([features.model_dump()])
    input_data = pd.DataFrame(input_data)

    ordinal_columns = [
        'Parental_Involvement', 'Access_to_Resources', 'Motivation_Level', 
        'Family_Income', 'Teacher_Quality', 'Peer_Influence', 
        'Parental_Education_Level', 'Distance_from_Home'
    ]
    binary_columns = [
        'Extracurricular_Activities', 'Internet_Access', 
        'School_Type', 'Learning_Disabilities', 'Gender'
    ]

    ord_encoder = OrdinalEncoder()
    input_data.loc[:, ordinal_columns] = ord_encoder.fit_transform(input_data[ordinal_columns])

    label_encoder = LabelEncoder()
    for column in binary_columns:
        input_data.loc[:,column] = label_encoder.fit_transform(input_data[column])

    input_data = input_data.astype('float64')
    preds = model.predict(input_data)

    return float(preds[0])

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable):
    start_time = time.time()
    request_body = await request.body()
    response: Response = await call_next(request)
    response_body = b""
    async for chunk in response.body_iterator:  # type: ignore
        response_body += chunk

    process_time = time.time() - start_time
    log_data = {
        "latency": process_time,
        "request": request_body.decode(),
        "method": request.method,
        "response": response_body.decode()
    }
    task = BackgroundTask(log_info, log_data)
    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
        background=task,
    )

@app.post("/predict")
def predict_endpoint(features: Features):
    try:
        pred = predict(features)
        result = {
            'score': pred,
            'model_version': RUN_ID
        }
        logger.info(f"Prediction made: {result['score']} using model version {RUN_ID}")
        return result
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
