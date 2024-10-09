import requests
import asyncio
import httpx

import pytest

API_URL = "http://127.0.0.1:8000/predict"

data = {
    "Hours_Studied": 5.0,
    "Attendance": 90.0,
    "Parental_Involvement": "High",
    "Access_to_Resources": "Medium",
    "Extracurricular_Activities": True,
    "Sleep_Hours": 7.0,
    "Previous_Scores": 85.0,
    "Motivation_Level": "High",
    "Internet_Access": True,
    "Tutoring_Sessions": 3,
    "Family_Income": "Medium",
    "Teacher_Quality": "High",
    "School_Type": "Public",
    "Peer_Influence": "Positive",
    "Physical_Activity": 2,
    "Learning_Disabilities": False,
    "Parental_Education_Level": "College",
    "Distance_from_Home": "Near",
    "Gender": "Male"
}

def test_predict_success():
    response = requests.post(API_URL, json=data)

    assert response.status_code == 200
    result = response.json()
    assert "score" in result
    assert "model_version" in result
    assert isinstance(result["score"], (float, int))

def test_predict_data_types():
    invalid_data = {
        "Hours_Studied": "five",  # Invalid string input
        "Attendance": 90.0,
        "Parental_Involvement": "High",
        "Access_to_Resources": "Medium",
        "Extracurricular_Activities": True,
        "Sleep_Hours": 7.0,
        "Previous_Scores": 85.0,
        "Motivation_Level": "High",
        "Internet_Access": True,
        "Tutoring_Sessions": 3,
        "Family_Income": "Medium",
        "Teacher_Quality": "High",
        "School_Type": "Public",
        "Peer_Influence": "Positive",
        "Physical_Activity": 2,
        "Learning_Disabilities": False,
        "Parental_Education_Level": "College",
        "Distance_from_Home": "Near",
        "Gender": "Male"
    }

    response = requests.post(API_URL, json=invalid_data)
    assert response.status_code == 422

def test_predict_missing_fields():
    incomplete_data = {
        "Hours_Studied": 5.0,
        "Parental_Involvement": "High"
    }

    response = requests.post(API_URL, json=incomplete_data)
    assert response.status_code == 422

 
@pytest.mark.parametrize("field, value", [
    ("Hours_Studied", -1.0),  # Negative value
    ("Hours_Studied", 1e40),  # Larger than 1e38
    ("Attendance", -5.0),     # Negative value
    ("Attendance", 1e40),     # Larger than 1e38
    ("Sleep_Hours", -3.0),    # Negative value
    ("Sleep_Hours", 1e40),    # Larger than 1e38
    ("Physical_Activity", -2.0),  # Negative value
    ("Physical_Activity", 1e40),  # Larger than 1e38
    ("Previous_Scores", -10.0),   # Negative value
    ("Previous_Scores", 1e40),    # Larger than 1e38
])
def test_edge_case_large_and_negative_numbers(field, value):
    # Base valid data
    data = {
        "Hours_Studied": 6.0,
        "Attendance": 90.0,
        "Parental_Involvement": "High",
        "Access_to_Resources": "Medium",
        "Extracurricular_Activities": True,
        "Sleep_Hours": 7.0,
        "Previous_Scores": 85.0,
        "Motivation_Level": "High",
        "Internet_Access": True,
        "Tutoring_Sessions": 3,
        "Family_Income": "Medium",
        "Teacher_Quality": "High",
        "School_Type": "Public",
        "Peer_Influence": "Positive",
        "Physical_Activity": 2,
        "Learning_Disabilities": False,
        "Parental_Education_Level": "College",
        "Distance_from_Home": "Near",
        "Gender": "Male"
    }

    # Replace the test field with the parametric value
    data[field] = value

    response = requests.post(API_URL, json=data)
    
    # Assert that the response status code is 422 Unprocessable Entity
    assert response.status_code == 422, f"Expected 422, but got {response.status_code} for field {field} with value {value}"

def test_empty_input_data():
    response = requests.post(API_URL, json={})  # Empty input
    assert response.status_code == 422

async def make_request(client):
    response = await client.post(API_URL, json=data)
    return response.status_code

@pytest.mark.asyncio
async def test_concurrent_requests():
    async with httpx.AsyncClient() as client:
        tasks = [make_request(client) for _ in range(200)]  # Simulate 200 concurrent requests
        responses = await asyncio.gather(*tasks)

    for status in responses:
        assert status == 200
