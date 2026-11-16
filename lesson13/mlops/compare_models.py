import hashlib
from pathlib import Path

import mlflow
import mlflow.sklearn

from sklearn.datasets import make_classification
from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# -------------------------------------
# 1. Configure MLflow
# -------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MLFLOW_DIR = PROJECT_ROOT / "lesson13" / "mlops"

DB_PATH = MLFLOW_DIR / "mlflow.db"
TRACKING_URI = f"sqlite:///{DB_PATH.as_posix()}"

mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment("customer-churn-model-comparison")


# -------------------------------------
# 2. Generate identical dataset
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

dataset_hash = hashlib.sha256(
    X.tobytes() + y.tobytes()
).hexdigest()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    stratify=y,
    random_state=42,
)


# -------------------------------------
# 3. Define candidate models
# -------------------------------------

models = {
    "logistic-regression": make_pipeline(
        StandardScaler(),
        LogisticRegression(
            max_iter=1000,
            random_state=42,
        ),
    ),
    "random-forest": RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1,
    ),
    "gradient-boosting": GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42,
    ),
}


# -------------------------------------
# 4. Train and track each model
# -------------------------------------

results = []

for model_name, model in models.items():

    with mlflow.start_run(run_name=model_name) as run:

        print(f"\nTraining: {model_name}")

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

        mlflow.log_param("algorithm", model_name)
        mlflow.log_param("dataset_sha256", dataset_hash)
        mlflow.log_params(model.get_params(deep=False))
        mlflow.log_metrics(metrics)

        # Explicitly trust the sklearn tree storage type
        # only for locally trained tree-based models.
        trusted_types = (
            ["sklearn.tree._tree.Tree"]
            if model_name in ("random-forest", "gradient-boosting")
            else []
        )

        mlflow.sklearn.log_model(
            sk_model=model,
            name="churn_model",
            input_example=X_train[:3],
            skops_trusted_types=trusted_types,
        )

        results.append({
            "model": model_name,
            "run_id": run.info.run_id,
            **metrics,
        })


# -------------------------------------
# 5. Print comparison
# -------------------------------------

print("\nMODEL COMPARISON")
print("-" * 75)

print(
    f"{'Model':<22}"
    f"{'Accuracy':>10}"
    f"{'Precision':>11}"
    f"{'Recall':>10}"
    f"{'AUC':>10}"
)

for result in results:
    print(
        f"{result['model']:<22}"
        f"{result['accuracy']:>10.4f}"
        f"{result['precision']:>11.4f}"
        f"{result['recall']:>10.4f}"
        f"{result['auc']:>10.4f}"
    )

best_model = max(results, key=lambda x: x["auc"])

print("\nBest model by AUC:")
print(best_model["model"])
print("Run ID:", best_model["run_id"])
