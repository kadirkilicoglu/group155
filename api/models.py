from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_role_id = Column(Integer, ForeignKey("user_roles.role_id"))
    user_email = Column(String, unique=True)
    user_first_name = Column(String)
    user_last_name = Column(String)
    user_hashed_password = Column(String)

    role = relationship("UserRole", back_populates="users")
    feedbacks = relationship("ModelFeedback", back_populates="user")
    entries = relationship("Entry", back_populates="assigned_doctor")


class UserRole(Base):
    __tablename__ = "user_roles"

    role_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_name = Column(String, unique=True)
    role_description = Column(String)

    can_create_user = Column(Boolean, nullable=False, server_default='false')
    can_edit_user = Column(Boolean, nullable=False, server_default='false')
    can_delete_user = Column(Boolean, nullable=False, server_default='false')
    can_view_user = Column(Boolean, nullable=False, server_default='false')

    can_create_role = Column(Boolean, nullable=False, server_default='false')
    can_edit_role = Column(Boolean, nullable=False, server_default='false')
    can_delete_role = Column(Boolean, nullable=False, server_default='false')
    can_view_role = Column(Boolean, nullable=False, server_default='false')

    can_create_patient = Column(Boolean, nullable=False, server_default='false')
    can_edit_patient = Column(Boolean, nullable=False, server_default='false')
    can_delete_patient = Column(Boolean, nullable=False, server_default='false')
    can_view_patient = Column(Boolean, nullable=False, server_default='false')

    can_create_entry = Column(Boolean, nullable=False, server_default='false')
    can_edit_entry = Column(Boolean, nullable=False, server_default='false')
    can_delete_entry = Column(Boolean, nullable=False, server_default='false')
    can_view_entry = Column(Boolean, nullable=False, server_default='false')

    can_create_prediction = Column(Boolean, nullable=False, server_default='false')
    can_edit_prediction = Column(Boolean, nullable=False, server_default='false')
    can_delete_prediction = Column(Boolean, nullable=False, server_default='false')
    can_view_prediction = Column(Boolean, nullable=False, server_default='false')

    can_create_feedback = Column(Boolean, nullable=False, server_default='false')
    can_edit_feedback = Column(Boolean, nullable=False, server_default='false')
    can_delete_feedback = Column(Boolean, nullable=False, server_default='false')
    can_view_feedback = Column(Boolean, nullable=False, server_default='false')

    can_create_report = Column(Boolean, nullable=False, server_default='false')
    can_edit_report = Column(Boolean, nullable=False, server_default='false')
    can_delete_report = Column(Boolean, nullable=False, server_default='false')
    can_view_report = Column(Boolean, nullable=False, server_default='false')


    users = relationship("User", back_populates="role")


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_first_name = Column(String)
    patient_last_name = Column(String)
    patient_gender = Column(String)
    patient_birth_date = Column(String)
    patient_email = Column(String, unique=True)

    entries = relationship("Entry", back_populates="patient")


class Entry(Base):
    __tablename__ = "entries"

    entry_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    entry_patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    entry_assigned_doctor_id = Column(Integer, ForeignKey("users.user_id"))
    entry_date = Column(String)

    entry_arrival_mode = Column(String)
    entry_injury = Column(String)
    entry_chief_complaint = Column(String)
    entry_patient_mental = Column(String)
    entry_patient_pain = Column(String)
    entry_nrs_pain = Column(String)
    entry_sbp = Column(String)
    entry_dbp = Column(String)
    entry_hr = Column(String)
    entry_rr = Column(String)
    entry_bt = Column(String)

    model_predictions = relationship("ModelPrediction", back_populates="entry")
    generated_reports = relationship("GeneratedReport", back_populates="entry")
    assigned_doctor = relationship("User", back_populates="entries")
    patient = relationship("Patient", back_populates="entries")



class ModelPrediction(Base):
    __tablename__ = "model_predictions"

    prediction_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prediction_entry_id = Column(Integer, ForeignKey("entries.entry_id"))
    prediction_label = Column(String)

    entry = relationship("Entry", back_populates="model_predictions")



class ModelFeedback(Base):
    __tablename__ = "model_feedbacks"

    feedback_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    feedback_user_id = Column(Integer, ForeignKey("users.user_id"))
    feedback_model_prediction_id = Column(Integer, ForeignKey("model_predictions.prediction_id"))
    feedback_label = Column(String)

    user = relationship("User", back_populates="feedbacks")
    

class GeneratedReport(Base):
    __tablename__ = "generated_reports"

    report_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    report_entry_id = Column(Integer, ForeignKey("entries.entry_id"))
    report_model_prediction_id = Column(Integer, ForeignKey("model_predictions.prediction_id"))
    report_content = Column(String)
    report_date = Column(String)

    entry = relationship("Entry", back_populates="generated_reports")