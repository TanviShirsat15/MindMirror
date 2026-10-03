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