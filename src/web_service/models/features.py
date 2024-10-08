# models/features.py
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class ParentalInvolvement(str, Enum):
    low = 'Low'
    medium = 'Medium'
    high = 'High'

class AccessToResources(str, Enum):
    low = 'Low'
    medium = 'Medium'
    high = 'High'

class MotivationLevel(str, Enum):
    low = 'Low'
    medium = 'Medium'
    high = 'High'

class FamilyIncome(str, Enum):
    low = 'Low'
    medium = 'Medium'
    high = 'High'

class TeacherQuality(str, Enum):
    low = 'Low'
    medium = 'Medium'
    high = 'High'

class SchoolType(str, Enum):
    public = 'Public'
    private = 'Private'

class PeerInfluence(str, Enum):
    positive = 'Positive'
    neutral = 'Neutral'
    negative = 'Negative'

class ParentalEducationLevel(str, Enum):
    high_school = 'High School'
    college = 'College'
    postgraduate = 'Postgraduate'

class DistanceFromHome(str, Enum):
    near = 'Near'
    moderate = 'Moderate'
    far = 'Far'

class Gender(str, Enum):
    male = 'Male'
    female = 'Female'

class Features(BaseModel):
    hours_studied: float = Field(..., alias='Hours_Studied')
    attendance: float = Field(..., alias='Attendance')
    parental_involvement: ParentalInvolvement = Field(..., alias='Parental_Involvement')
    access_to_resources: AccessToResources = Field(..., alias='Access_to_Resources')
    extracurricular_activities: bool = Field(..., alias='Extracurricular_Activities')
    sleep_hours: float = Field(..., alias='Sleep_Hours')
    physical_activity: float = Field(..., alias='Physical_Activity')
    previous_scores: Optional[float] = Field(None, alias='Previous_Scores')
    motivation_level: MotivationLevel = Field(..., alias='Motivation_Level')
    internet_access: bool = Field(..., alias='Internet_Access')
    tutoring_sessions: int = Field(..., alias='Tutoring_Sessions')
    family_income: FamilyIncome = Field(..., alias='Family_Income')
    teacher_quality: TeacherQuality = Field(..., alias='Teacher_Quality')
    school_type: SchoolType = Field(..., alias='School_Type')
    peer_influence: PeerInfluence = Field(..., alias='Peer_Influence')
    learning_disabilities: bool = Field(..., alias='Learning_Disabilities')
    parental_education_level: ParentalEducationLevel = Field(..., alias='Parental_Education_Level')
    distance_from_home: DistanceFromHome = Field(..., alias='Distance_from_Home')
    gender: Gender = Field(..., alias='Gender')
