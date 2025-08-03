from fastapi import APIRouter, Depends, HTTPException, Path, status, Form, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from api.models import Base, ModelPrediction, Entry
from api.request_models import TriagePredictionRequest, ModelPredictionRequest
from api.database import engine, SessionLocal
from typing import Annotated
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from api.routers.authentication import get_current_user, require_permission
import pandas as pd
import numpy as np
import joblib


router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"]
)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_session)]
UserDep = Annotated[dict, Depends(get_current_user)]


SELECTED_FEATURES = [
    'ktas_rn', 'mistriage', 'error_group', 'nrs_pain', 'length_of_stay_min',
    'age', 'disposition', 'hr', 'sbp', 'bt', 'ktas_duration_min', 'mental', 'injury'
]


NUMERIC_FEATURES = SELECTED_FEATURES.copy()


def preprocess_entry_data(entry_dict: dict, scaler) -> np.ndarray:
    df = pd.DataFrame([entry_dict])
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.strip()
    for col in NUMERIC_FEATURES:
        df[col] = pd.to_numeric(df.get(col), errors="coerce")
    df = df.fillna(df.mean(numeric_only=True))
    df = df[SELECTED_FEATURES]
    X_scaled = scaler.transform(df)
    return X_scaled


def predict_triage(entry_data: np.ndarray, model) -> str:
    prediction_prob = model.predict(entry_data)
    predicted_class = np.argmax(prediction_prob, axis=1)[0]
    emergency_color_dict = {
        0: "Red",
        1: "Yellow",
        2: "Green",
    }
    return emergency_color_dict.get(predicted_class, "Unknown")



@router.post("/get_emergency_color_prediction_without_auth")
async def get_emergency_color_prediction(prediction_request: TriagePredictionRequest, session: SessionDep, request: Request):
    """
    Endpoint to get the emergency color prediction.
    """

    scaler = request.app.state.scaler
    model = request.app.state.triage_model

    entry_data = preprocess_entry_data(prediction_request.model_dump(), scaler)
    emergency_color = predict_triage(entry_data, model)

    return {"prediction": emergency_color}


@router.post("/get_emergency_color_prediction")
async def get_emergency_color_prediction(prediction_request: TriagePredictionRequest, user: UserDep, session: SessionDep, request: Request):
    """
    Endpoint to get the emergency color prediction.
    """
    require_permission(user, "can_create_prediction")

    scaler = request.app.state.scaler
    model = request.app.state.triage_model

    entry_data = preprocess_entry_data(prediction_request.model_dump(), scaler)
    emergency_color = predict_triage(entry_data, model)

    return {"prediction": emergency_color}


@router.get("/get_predictions", status_code=status.HTTP_200_OK)
async def get_predictions(user: UserDep, session: SessionDep):
    """
    Endpoint to retrieve all model predictions.
    """
    require_permission(user, "can_view_prediction")
    predictions = session.query(ModelPrediction).all()
    return predictions


@router.get("/get_prediction/{prediction_id}", status_code=status.HTTP_200_OK)
async def get_prediction(prediction_id: int, user: UserDep, session: SessionDep):
    """
    Endpoint to retrieve a specific model prediction by ID.
    """
    require_permission(user, "can_view_prediction")

    prediction = session.query(ModelPrediction).filter(ModelPrediction.prediction_id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediction not found")
    
    return prediction


@router.post("/create_prediction", status_code=status.HTTP_201_CREATED)
async def create_prediction(prediction_request: ModelPredictionRequest, user: UserDep, session: SessionDep):
    """
    Endpoint to create a model prediction.
    """
    require_permission(user, "can_create_prediction")

    entry = session.query(Entry).filter(Entry.entry_id == prediction_request.entry_id).first()

    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    
    prediction = ModelPrediction(**prediction_request.model_dump())

    session.add(prediction)
    session.commit()
    session.refresh(prediction)
    return prediction
    

@router.put("/update_prediction/{prediction_id}", status_code=status.HTTP_200_OK)
async def update_prediction(prediction_id: int, prediction_request: ModelPredictionRequest, user: UserDep, session: SessionDep):
    """
    Endpoint to update an existing model prediction.
    """
    require_permission(user, "can_edit_prediction")

    existing_prediction = session.query(ModelPrediction).filter(ModelPrediction.prediction_id == prediction_id).first()

    if not existing_prediction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediction not found")
    
    for key, value in prediction_request.model_dump().items():
        setattr(existing_prediction, key, value)
    
    session.commit()
    session.refresh(existing_prediction)
    return existing_prediction


@router.delete("/delete_prediction/{prediction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prediction(prediction_id: int, user: UserDep, session: SessionDep):
    """
    Endpoint to delete an existing model prediction.
    """
    require_permission(user, "can_delete_prediction")

    existing_prediction = session.query(ModelPrediction).filter(ModelPrediction.prediction_id == prediction_id).first()

    if not existing_prediction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediction not found")
    
    session.delete(existing_prediction)
    session.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    