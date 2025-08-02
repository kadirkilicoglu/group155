from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str
    token_type: str


class UserRoleRequest(BaseModel):

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