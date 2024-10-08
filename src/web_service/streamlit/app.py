import streamlit as st
import requests  # If you're making an API call

st.title("Student Performance Prediction")

# Input fields for user input
hours_studied = st.number_input("Hours Studied", min_value=0.0)
attendance = st.number_input("Attendance", min_value=0.0)
parental_involvement = st.selectbox("Parental Involvement", ['Low', 'Medium', 'High'])
access_to_resources = st.selectbox("Access to Resources", ['Low', 'Medium', 'High'])
extracurricular_activities = st.checkbox("Extracurricular Activities")
sleep_hours = st.number_input("Sleep Hours", min_value=0.0)
previous_scores = st.number_input("Previous Scores", min_value=0.0)
motivation_level = st.selectbox("Motivation Level", ['Low', 'Medium', 'High'])
internet_access = st.checkbox("Internet Access")
tutoring_sessions = st.number_input("Tutoring Sessions", min_value=0)
family_income = st.selectbox("Family Income", ['Low', 'Medium', 'High'])
teacher_quality = st.selectbox("Teacher Quality", ['Low', 'Medium', 'High'])
school_type = st.selectbox("School Type", ['Public', 'Private'])
peer_influence = st.selectbox("Peer Influence", ['Positive', 'Neutral', 'Negative'])
physical_activity = st.number_input("Physical Activity", min_value=0.0)
learning_disabilities = st.checkbox("Learning Disabilities")
parental_education_level = st.selectbox("Parental Education Level", ['High School', 'College', 'Postgraduate'])
distance_from_home = st.selectbox("Distance from Home", ['Near', 'Moderate', 'Far'])
gender = st.selectbox("Gender", ['Male', 'Female'])

# Button to make a prediction
if st.button("Predict"):
    # Prepare the data for the API
    features = {
        "Hours_Studied": hours_studied,
        "Attendance": attendance,
        "Parental_Involvement": parental_involvement,
        "Access_to_Resources": access_to_resources,
        "Extracurricular_Activities": int(extracurricular_activities),
        "Sleep_Hours": sleep_hours,
        "Previous_Scores": previous_scores,
        "Motivation_Level": motivation_level,
        "Internet_Access": int(internet_access),
        "Tutoring_Sessions": tutoring_sessions,
        "Family_Income": family_income,
        "Teacher_Quality": teacher_quality,
        "School_Type": school_type,
        "Peer_Influence": peer_influence,
        "Physical_Activity": physical_activity,
        "Learning_Disabilities": int(learning_disabilities),
        "Parental_Education_Level": parental_education_level,
        "Distance_from_Home": distance_from_home,
        "Gender": gender,
    }

    # Call the prediction API (replace with your actual API endpoint)
    api_url = "http://fastapi:8000/predict"
    response = requests.post(api_url, json=features)

    if response.status_code == 200:
        result = response.json().get("score")
        st.success(f"The predicted performance is: {result}")
    else:
        st.error("An error occurred while making the prediction.")
