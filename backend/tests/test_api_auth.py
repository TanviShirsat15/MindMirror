import jwt

from app.config import settings
from app.models.user import User


def test_register_login_and_me(client):
    email = "api_test_user@mindmirror.com"
    password = "TestPassword123!"

    # Register
    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "API Test User",
        },
    )

    assert response.status_code == 201

    data = response.json()

    # Password must never be returned
    assert "password" not in data
    assert "password_hash" not in data
    assert data["email"] == email

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    token_data = response.json()

    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # Access /me using the JWT
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token_data['access_token']}"
        },
    )

    assert response.status_code == 200
    assert response.json()["email"] == email


def test_me_requires_authentication(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_duplicate_registration_returns_409(client):
    email = "duplicate@mindmirror.com"
    password = "TestPassword123!"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Duplicate Test",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Duplicate Test",
        },
    )

    assert response.status_code == 409


def test_wrong_password_returns_generic_401(client):
    email = "wrong_password@mindmirror.com"
    password = "TestPassword123!"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Wrong Password Test",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_unknown_email_returns_generic_401(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "does_not_exist@mindmirror.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_password_is_stored_as_argon2_hash(client, db_session):
    email = "hash_test@mindmirror.com"
    password = "TestPassword123!"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Hash Test",
        },
    )

    assert response.status_code == 201

    user = db_session.query(User).filter(User.email == email).first()

    assert user is not None
    assert user.password_hash != password
    assert user.password_hash.startswith("$argon2")


def test_jwt_contains_subject_and_expiration(client):
    email = "jwt_claims@mindmirror.com"
    password = "TestPassword123!"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "JWT Claims Test",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == 200

    token = response.json()["access_token"]

    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=["HS256"],
    )

    assert "sub" in payload
    assert "exp" in payload
    assert payload["sub"].isdigit()


def test_malformed_jwt_returns_401(client):
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer this-is-not-a-valid-jwt"
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"


def test_invalid_signature_jwt_returns_401(client):
    email = "invalid_signature@mindmirror.com"
    password = "TestPassword123!"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Invalid Signature Test",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == 200

    token = response.json()["access_token"]

    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=["HS256"],
    )

    tampered_token = jwt.encode(
        payload,
        "wrong-secret-for-testing-32-bytes-minimum!",
        algorithm="HS256",
    )

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {tampered_token}"
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"


def test_expired_jwt_returns_401(client):
    email = "expired_jwt@mindmirror.com"
    password = "TestPassword123!"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Expired JWT Test",
        },
    )
    assert response.status_code == 201

    expired_token = jwt.encode(
        {
            "sub": "1",
            "exp": 1,
        },
        settings.JWT_SECRET,
        algorithm="HS256",
    )

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {expired_token}"
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"

def test_login_rate_limit_returns_429(client):
    email = "rate_limit@mindmirror.com"
    password = "TestPassword123!"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Rate Limit Test",
        },
    )
    assert response.status_code == 201

    # Five login requests are allowed per minute.
    for _ in range(5):
        response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )
        assert response.status_code == 200

    # The sixth request must be rate limited.
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 429
    assert response.json()["detail"] == (
        "Too many requests. Please try again later."
    )