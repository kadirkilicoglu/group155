from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str
    token_type: str


class UserRoleRequest(BaseModel):

    role_id: int = Field(..., example=1, description="Unique identifier for the user role")
    role_name: str = Field(..., example="Admin", description="Name of the user role", min_length=1, max_length=50)
    role_description: str = Field(..., example="Administrator with full access", description="Description of the user role", min_length=1, max_length=255, nullable=True)

    can_create_user: bool = Field(default=False, example=True, description="Permission to create a user")
    can_edit_user: bool = Field(default=False, example=True, description="Permission to edit a user")
    can_delete_user: bool = Field(default=False, example=True, description="Permission to delete a user")
    can_view_user: bool = Field(default=False, example=True, description="Permission to view a user")

    can_create_role: bool = Field(default=False, example=True, description="Permission to create a user role")
    can_edit_role: bool = Field(default=False, example=True, description="Permission to edit a user role")
    can_delete_role: bool = Field(default=False, example=True, description="Permission to delete a user role")
    can_view_role: bool = Field(default=False, example=True, description="Permission to view a user role")

    can_create_patient: bool = Field(default=False, example=True, description="Permission to create a patient")
    can_edit_patient: bool = Field(default=False, example=True, description="Permission to edit a patient")
    can_delete_patient: bool = Field(default=False, example=True, description="Permission to delete a patient")
    can_view_patient: bool = Field(default=False, example=True, description="Permission to view a patient")

    can_create_entry: bool = Field(default=False, example=True, description="Permission to create an entry")
    can_edit_entry: bool = Field(default=False, example=True, description="Permission to edit an entry")
    can_delete_entry: bool = Field(default=False, example=True, description="Permission to delete an entry")
    can_view_entry: bool = Field(default=False, example=True, description="Permission to view an entry")

    can_create_prediction: bool = Field(default=False, example=True, description="Permission to create a prediction")
    can_edit_prediction: bool = Field(default=False, example=True, description="Permission to edit a prediction")
    can_delete_prediction: bool = Field(default=False, example=True, description="Permission to delete a prediction")
    can_view_prediction: bool = Field(default=False, example=True, description="Permission to view a prediction")

    can_create_feedback: bool = Field(default=False, example=True, description="Permission to create feedback")
    can_edit_feedback: bool = Field(default=False, example=True, description="Permission to edit feedback")
    can_delete_feedback: bool = Field(default=False, example=True, description="Permission to delete feedback")
    can_view_feedback: bool = Field(default=False, example=True, description="Permission to view feedback")

    can_create_report: bool = Field(default=False, example=True, description="Permission to create a report")
    can_edit_report: bool = Field(default=False, example=True, description="Permission to edit a report")
    can_delete_report: bool = Field(default=False, example=True, description="Permission to delete a report")
    can_view_report: bool = Field(default=False, example=True, description="Permission to view a report")


class RoleRequest(BaseModel):

    role_name: str = Field(..., example="Admin", description="Name of the user role", min_length=1, max_length=50)
    role_description: str = Field(..., example="Administrator with full access", description="Description of the user role", min_length=1, max_length=255, nullable=True)

    can_create_user: bool = Field(default=False, example=True, description="Permission to create a user")
    can_edit_user: bool = Field(default=False, example=True, description="Permission to edit a user")
    can_delete_user: bool = Field(default=False, example=True, description="Permission to delete a user")
    can_view_user: bool = Field(default=False, example=True, description="Permission to view a user")

    can_create_role: bool = Field(default=False, example=True, description="Permission to create a user role")
    can_edit_role: bool = Field(default=False, example=True, description="Permission to edit a user role")
    can_delete_role: bool = Field(default=False, example=True, description="Permission to delete a user role")
    can_view_role: bool = Field(default=False, example=True, description="Permission to view a user role")

    can_create_patient: bool = Field(default=False, example=True, description="Permission to create a patient")
    can_edit_patient: bool = Field(default=False, example=True, description="Permission to edit a patient")
    can_delete_patient: bool = Field(default=False, example=True, description="Permission to delete a patient")
    can_view_patient: bool = Field(default=False, example=True, description="Permission to view a patient")

    can_create_entry: bool = Field(default=False, example=True, description="Permission to create an entry")
    can_edit_entry: bool = Field(default=False, example=True, description="Permission to edit an entry")
    can_delete_entry: bool = Field(default=False, example=True, description="Permission to delete an entry")
    can_view_entry: bool = Field(default=False, example=True, description="Permission to view an entry")

    can_create_prediction: bool = Field(default=False, example=True, description="Permission to create a prediction")
    can_edit_prediction: bool = Field(default=False, example=True, description="Permission to edit a prediction")
    can_delete_prediction: bool = Field(default=False, example=True, description="Permission to delete a prediction")
    can_view_prediction: bool = Field(default=False, example=True, description="Permission to view a prediction")

    can_create_feedback: bool = Field(default=False, example=True, description="Permission to create feedback")
    can_edit_feedback: bool = Field(default=False, example=True, description="Permission to edit feedback")
    can_delete_feedback: bool = Field(default=False, example=True, description="Permission to delete feedback")
    can_view_feedback: bool = Field(default=False, example=True, description="Permission to view feedback")

    can_create_report: bool = Field(default=False, example=True, description="Permission to create a report")
    can_edit_report: bool = Field(default=False, example=True, description="Permission to edit a report")
    can_delete_report: bool = Field(default=False, example=True, description="Permission to delete a report")
    can_view_report: bool = Field(default=False, example=True, description="Permission to view a report")


class UserRequest(BaseModel):
    username : str
    first_name : str
    last_name : str
    password : str
    role : int


class PatientRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    gender: str = Field(..., description="Gender of the patient")
    birth_date: str = Field(..., description="Birth date of the patient in YYYY-MM-DD format")
    email: str = Field(..., description="Email of the patient")


class EntryRequest(BaseModel):

    patient_id: int = Field(..., description="ID of the patient associated with the entry")
    assigned_doctor_id: int = Field(..., description="ID of the doctor assigned to the entry")
    entry_date: str = Field(..., description="Date of the entry")
    entry_arrival_mode: str = Field(..., description="Arrival mode of the patient")
    entry_injury: str = Field(..., description="Injury details of the patient")
    entry_chief_complaint: str = Field(..., description="Chief complaint of the patient")
    entry_patient_mental: str = Field(..., description="Mental status of the patient")
    entry_patient_pain: str = Field(..., description="Pain status of the patient")
    entry_nrs_pain: str = Field(..., description="NRS pain score of the patient")
    entry_sbp: str = Field(..., description="Systolic blood pressure of the patient")
    entry_dbp: str = Field(..., description="Diastolic blood pressure of the patient")
    entry_hr: str = Field(..., description="Heart rate of the patient")
    entry_rr: str = Field(..., description="Respiratory rate of the patient")
    entry_bt: str = Field(..., description="Body temperature of the patient")


class TriagePredictionRequest(BaseModel):
    ktas_rn: int = Field(..., description="KTAS RN value")
    mistriage: int = Field(..., description="Mistriage value")
    error_group: int = Field(..., description="Error group value")
    nrs_pain: int = Field(..., description="NRS pain value")
    length_of_stay_min: int = Field(..., description="Length of stay in minutes")
    age: int = Field(..., description="Age of the patient")
    disposition: str = Field(..., description="Disposition of the patient")
    hr: float = Field(..., description="Heart rate")
    sbp: float = Field(..., description="Systolic blood pressure")
    bt: float = Field(..., description="Body temperature")
    ktas_duration_min: int = Field(..., description="KTAS duration in minutes")
    mental: str = Field(..., description="Mental status")
    injury: str = Field(..., description="Injury status")


class ModelPredictionRequest(BaseModel):
    entry_id: int = Field(..., description="ID of the entry for which the prediction is made")
    label: str = Field(..., description="Predicted label for the entry")