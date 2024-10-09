from unittest.mock import patch
import requests

API_URL = "http://127.0.0.1:8000/predict"

# Example input data for testing
data = {
    "hours_studied": 5.0,
    "attendance": 90.0,
    "parental_involvement": "High",
    "access_to_resources": "Medium",
    "extracurricular_activities": True,
    "sleep_hours": 7.0,
    "previous_scores": 85.0,
    "motivation_level": "High",
    "internet_access": True,
    "tutoring_sessions": 3,
    "family_income": "Medium",
    "teacher_quality": "High",
    "school_type": "Public",
    "peer_influence": "Positive",
    "physical_activity": 2,
    "learning_disabilities": False,
    "parental_education_level": "College",
    "distance_from_home": "Near",
    "gender": "Male"
}

# Mock MLflow and Logstash integration
@patch('mlflow.pyfunc.load_model')
@patch('logstash.TCPLogstashHandler')
def test_prediction_integration(mock_logstash_handler, mock_load_model):
    # Mock the MLflow model prediction
    mock_model = mock_load_model.return_value
    mock_model.predict.return_value = [85.0]  # Mock prediction result

    # Send a POST request to the /predict endpoint
    response = requests.post(API_URL, json=data)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the prediction result is correct
    result = response.json()
    assert result['score'] == 85.0  # Ensure it matches the mock result

    # Check if Logstash received the expected log message
    mock_logstash_handler().emit.assert_called()
