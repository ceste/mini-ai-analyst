from contextlib import asynccontextmanager
from pathlib import Path

import mlflow
import mlflow.sklearn
import numpy as np

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# -------------------------------------
# Configuration
# -------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "lesson13" / "mlops" / "mlflow.db"

mlflow.set_tracking_uri(f"sqlite:///{DB_PATH.as_posix()}")

MODEL_NAME = "customer-churn-classifier"
MODEL_ALIAS = "champion"

model = None


# -------------------------------------
# Load model at startup
# -------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model

    model_uri = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"

    print(f"Loading model: {model_uri}")

    # Only load artifacts from our trusted local registry.
    # model = mlflow.sklearn.load_model(
    #     model_uri,
    #     skops_trusted_types=[
    #         "sklearn.tree._tree.Tree",
    #     ],
    # )

    model = mlflow.sklearn.load_model(
        model_uri,
        dst_path=None,
    )

    print("Model loaded successfully")

    yield

    model = None


app = FastAPI(
    title="Churn Prediction API",
    version="1.0.0",
    lifespan=lifespan,
)


# -------------------------------------
# Request and response schemas
# -------------------------------------

class PredictionRequest(BaseModel):
    features: list[float] = Field(
        ...,
        min_length=12,
        max_length=12,
    )


class PredictionResponse(BaseModel):
    prediction: int
    churn_probability: float
    model_name: str
    model_alias: str


# -------------------------------------
# Endpoints
# -------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy" if model is not None else "unavailable",
        "model_loaded": model is not None,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):

    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded",
        )

    try:
        features = np.asarray(
            [request.features],
            dtype=np.float64,
        )

        if not np.isfinite(features).all():
            raise ValueError(
                "Features must contain only finite numbers"
            )

        prediction = int(model.predict(features)[0])

        probability = float(
            model.predict_proba(features)[0][1]
        )

        return PredictionResponse(
            prediction=prediction,
            churn_probability=probability,
            model_name=MODEL_NAME,
            model_alias=MODEL_ALIAS,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc
