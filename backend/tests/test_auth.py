from app.core.security import create_access_token, hash_password, verify_password


def test_password_hashing():
    password = "TestPassword123!"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword123!", hashed)


def test_jwt_creation():
    token = create_access_token("1")

    assert token
    assert isinstance(token, str)