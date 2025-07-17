from fastapi import FastAPI
from models import Base
from database import engine
from routers.prediction import router as prediction_router
from routers.admin import router as admin_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine)
    #ml_models[""] = ml_models.load_model("path/to/model")
    yield

    #ml_models.clear()


app = FastAPI(lifespan = lifespan)

app.include_router(prediction_router)
app.include_router(admin_router)