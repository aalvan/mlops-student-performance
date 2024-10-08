from pydantic import BaseModel, conint, condecimal
from enum import Enum

class Features(BaseModel):
    Hours_Studied: condecimal(gt=0)  # Positive float for hours studied
    Attendance: condecimal(ge=0, le=100)  # Percentage, between 0 and 100
    Parental_Involvement: str  # Categorical: Low, Medium, High
    Access_to_Resources: str  # Categorical: Low, Medium, High
    Extracurricular_Activities: str  # Categorical: Yes, No
    Sleep_Hours: condecimal(gt=0)  # Positive float for sleep hours
    Previous_Scores: condecimal(gt=0)  # Positive float for previous scores
    Motivation_Level: str  # Categorical: Low, Medium, High
    Internet_Access: str  # Categorical: Yes, No
    Tutoring_Sessions: conint(ge=0)  # Integer for number of tutoring sessions
    Family_Income: str  # Categorical: Low, Medium, High
    Teacher_Quality: str  # Categorical: Low, Medium, High
    School_Type: str  # Categorical: Public, Private
    Peer_Influence: str  # Categorical: Positive, Neutral, Negative
    Physical_Activity: condecimal(gt=0)  # Positive float for hours of physical activity
    Learning_Disabilities: str  # Categorical: Yes, No
    Parental_Education_Level: str  # Categorical: High School, College, Postgraduate
    Distance_from_Home: str  # Categorical: Near, Moderate, Far
    Gender: str  # Categorical: Male, Female
