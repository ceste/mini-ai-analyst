# import os
# import secrets

# from fastapi import FastAPI, Header, HTTPException

# app = FastAPI(title="AI Analyst Security Lab")


# @app.get("/health")
# def health():
#     return {"status": "healthy"}


# @app.get("/secure")
# def secure_endpoint(
#     x_api_key: str | None = Header(default=None),
# ):
#     expected_key = os.environ.get("AI_ANALYST_API_KEY")

#     if not expected_key:
#         raise HTTPException(
#             status_code=503,
#             detail="API key not configured",
#         )

#     if not x_api_key or not secrets.compare_digest(
#         x_api_key,
#         expected_key,
#     ):
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid API key",
#         )

#     return {
#         "message": "Authenticated successfully"
#     }


import os
import secrets

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI(title="AI Analyst Security Lab")


def authenticate(
    x_api_key: str | None = Header(default=None),
) -> str:
    """Authenticate the caller and return its role."""

    analyst_key = os.getenv("AI_ANALYST_KEY")
    admin_key = os.getenv("AI_ADMIN_KEY")

    if not analyst_key or not admin_key:
        raise HTTPException(
            status_code=503,
            detail="Authentication not configured",
        )

    if secrets.compare_digest(analyst_key, admin_key):
        raise HTTPException(
            status_code=503,
            detail="Authentication configuration invalid",
        )

    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API key",
        )

    if secrets.compare_digest(x_api_key, admin_key):
        return "admin"

    if secrets.compare_digest(x_api_key, analyst_key):
        return "analyst"

    raise HTTPException(
        status_code=401,
        detail="Invalid API key",
    )


def require_admin(
    role: str = Depends(authenticate),
) -> str:
    """Allow only authenticated administrators."""

    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin permission required",
        )

    return role


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/secure")
def secure_endpoint(
    role: str = Depends(authenticate),
):
    return {
        "message": "Authenticated successfully",
        "role": role,
    }


@app.get("/admin")
def admin_endpoint(
    role: str = Depends(require_admin),
):
    return {
        "message": "Welcome to admin dashboard",
        "role": role,
    }


# def test_detect_authorization_regression(client, monkeypatch):
#     from lesson12 import security_api

#     # Simulate a bug: every authenticated user becomes admin.
#     def broken_authenticate():
#         return "admin"

#     # Override FastAPI's dependency, not just the Python name.
#     app.dependency_overrides[security_api.authenticate] = (
#         broken_authenticate
#     )

#     try:
#         response = client.get(
#             "/admin",
#             headers={"X-API-Key": "test-analyst-key"},
#         )

#         # A secure application must reject an analyst.
#         assert response.status_code == 403

#     finally:
#         app.dependency_overrides.clear()
