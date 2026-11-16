from pathlib import Path

import mlflow
import mlflow.sklearn

from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "lesson13" / "mlops" / "mlflow.db"

mlflow.set_tracking_uri(f"sqlite:///{DB_PATH.as_posix()}")
mlflow.set_experiment("customer-churn-model-comparison")


X, y = make_classification(
    n_samples=5000,
    n_features=12,
    n_informative=7,
    n_redundant=3,
    weights=[0.80, 0.20],
    flip_y=0.02,
    random_state=42,
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    stratify=y,
    random_state=42,
)

# Intentionally weak model for validation testing.
model = DummyClassifier(strategy="prior")

with mlflow.start_run(run_name="intentionally-bad-candidate"):

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

    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        name="churn_model",
        input_example=X_train[:3],
    )

    registered = mlflow.register_model(
        model_uri=model_info.model_uri,
        name="customer-churn-classifier",
    )

    print("\nBad candidate metrics:", metrics)
    print("Registered version:", registered.version)
    print("Run ID:", mlflow.active_run().info.run_id)
