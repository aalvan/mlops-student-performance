import requests

# Define the API URL
api_url = "http://127.0.0.1:8000/predict"

# Example input data (Features to send to the API)
data = {
    "Hours_Studied": 10.5,
    "Attendance": 95,
    "Parental_Involvement": "High",
    "Access_to_Resources": "Medium",
    "Extracurricular_Activities": "Yes",
    "Sleep_Hours": 7.5,
    "Previous_Scores": 85.5,
    "Motivation_Level": "Medium",
    "Internet_Access": "Yes",
    "Tutoring_Sessions": 2,
    "Family_Income": "Medium",
    "Teacher_Quality": "High",
    "School_Type": "Public",
    "Peer_Influence": "Positive",
    "Physical_Activity": 3.5,
    "Learning_Disabilities": "No",
    "Parental_Education_Level": "College",
    "Distance_from_Home": "Moderate",
    "Gender": "Female"
}

# Send a POST request to the /predict endpoint
response = requests.post(api_url, json=data)

# Check if the request was successful
if response.status_code == 200:
    print(f"Prediction Result: {response.json()}")
else:
    print(f"Failed to get prediction, Status code: {response.status_code}, Error: {response.text}")
