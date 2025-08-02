from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
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


class UserRole(Base):
    __tablename__ = "user_roles"

    role_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_name = Column(String, unique=True)
    role_description = Column(String)

    users = relationship("User", back_populates="role")


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_first_name = Column(String)
    patient_last_name = Column(String)
    patient_gender = Column(String)
    patient_birth_date = Column(String)
    patient_email = Column(String, unique=True)


class Entry(Base):
    __tablename__ = "entries"

    entry_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    entry_patient_id = Column(Integer, ForeignKey("patients.patient_id"))
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


class ModelPrediction(Base):
    __tablename__ = "model_predictions"

    prediction_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prediction_entry_id = Column(Integer, ForeignKey("entries.entry_id"))
    prediction_label = Column(String)


class ModelFeedback(Base):
    __tablename__ = "model_feedbacks"

    feedback_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    feedback_user_id = Column(Integer, ForeignKey("users.user_id"))
    feedback_model_prediction_id = Column(Integer, ForeignKey("model_predictions.prediction_id"))
    feedback_label = Column(String)
    

class GeneratedReport(Base):
    __tablename__ = "generated_reports"

    report_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    report_entry_id = Column(Integer, ForeignKey("entries.entry_id"))
    report_model_prediction_id = Column(Integer, ForeignKey("model_predictions.prediction_id"))
    report_content = Column(String)
    report_date = Column(String)