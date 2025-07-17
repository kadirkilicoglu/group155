from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Base, ModelFeedback, Entry, ModelPrediction
from database import engine, SessionLocal
from typing import Annotated


router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_session)]


class ModelFeedbackRequest(BaseModel):
    feedback_user_id: int = Field(..., example=1, description="ID of the user providing feedback")
    feedback_model_prediction_id: int = Field(..., example=1, description="ID of the model prediction being reviewed")
    feedback_label: str = Field(..., example="Red or Yellow or Green", description = "Doctors' review over model prediction" , min_length=1, max_length=50)


@router.get("/get_feedbacks", status_code=status.HTTP_200_OK)
async def get_feedbacks(session: SessionDep):
    """
    Endpoint to retrieve all feedbacks.
    """
    feedbacks = session.query(ModelFeedback).all()
    return feedbacks


@router.post("/create_feedback", status_code=status.HTTP_201_CREATED)
async def create_feedback(feedback_request: ModelFeedbackRequest, session: SessionDep):
    """
    Endpoint to create a new feedback.
    """
    # NEEDS TO BE IMPLEMENTED: Check if the prediction exists and is valid
    existing_feedback = session.query(ModelFeedback).add_entity(Entry.entry_id).add_entity(ModelPrediction.prediction_id).filter()
    if existing_feedback:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Feedback already exists")
    
    feedback = ModelFeedback(**feedback_request.model_dump())

    session.add(feedback)
    session.commit()
    session.refresh(feedback)
    return feedback