import hashlib
import json
from pathlib import Path

import mlflow
import mlflow.sklearn
import numpy as np

from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


# -------------------------------------
# Configuration
# -------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MLFLOW_DIR = PROJECT_ROOT / "lesson13" / "mlops"
MLFLOW_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = MLFLOW_DIR / "mlflow.db"

TRACKING_URI = f"sqlite:///{DB_PATH.as_posix()}"

mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment("customer-churn-prediction")

# -------------------------------------
# 1. Generate synthetic churn data
# -------------------------------------

X, y = make_classification(
    n_samples=5000,
    n_features=12,
    n_informative=7,
    n_redundant=3,
    weights=[0.80, 0.20],
    flip_y=0.02,
    random_state=42,
)

feature_names = [f"feature_{i}" for i in range(X.shape[1])]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    stratify=y,
    random_state=42,
)

# Dataset fingerprint for reproducibility
dataset_hash = hashlib.sha256(
    X.tobytes() + y.tobytes()
).hexdigest()


# -------------------------------------
# 2. Configure model
# -------------------------------------

params = {
    "n_estimators": 100,
    "max_depth": 8,
    "min_samples_leaf": 5,
    "random_state": 42,
    "n_jobs": -1,
}

model = RandomForestClassifier(**params)


# -------------------------------------
# 3. Train and track experiment
# -------------------------------------

with mlflow.start_run(run_name="random-forest-baseline") as run:

    mlflow.log_params(params)

    mlflow.log_param("training_samples", len(X_train))
    mlflow.log_param("test_samples", len(X_test))
    mlflow.log_param("dataset_sha256", dataset_hash)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(
            y_test, predictions, zero_division=0
        ),
        "recall": recall_score(
            y_test, predictions, zero_division=0
        ),
        "auc": roc_auc_score(y_test, probabilities),
    }

    mlflow.log_metrics(metrics)

    # mlflow.sklearn.log_model(
    #     sk_model=model,
    #     name="churn_model",
    #     input_example=X_train[:3],
    # )

    mlflow.sklearn.log_model(
	    sk_model=model,
	    name="churn_model",
	    input_example=X_train[:3],
	    skops_trusted_types=[
	        "sklearn.tree._tree.Tree",
	    ],
	)

    mlflow.set_tags({
        "project": "mini-ai-analyst",
        "lesson": "13.6",
        "dataset": "synthetic",
        "algorithm": "random_forest",
    })

    print("\nExperiment completed")
    print(f"Run ID: {run.info.run_id}")
    print(f"Dataset SHA256: {dataset_hash}")

    print("\nMetrics:")
    print(json.dumps(metrics, indent=2))
