from datetime import date

from app.insights.insight_service import generate_insights
from app.models.user import User
from app.models.wellbeing_score import WellBeingScore


def register_and_login(client, email):
    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "TestPassword123!",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "TestPassword123!",
        },
    )
    assert response.status_code == 200

    return response.json()["access_token"]


def test_generate_insights_with_no_history(db_session):
    user = User(
        email="phase13_service@test.com",
        password_hash="test-password",
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    result = generate_insights(
        db=db_session,
        current_user=user,
        as_of=date.today(),
    )

    assert result["status"] == "success"
    assert result["insights"] == []
    assert (
        result["meta"]["disclaimer"]
        == "Insights describe patterns in your own historical data "
        "and are not medical or clinical measurements or advice."
    )


def test_generated_insights_requires_authentication(client):
    response = client.get("/api/insights/generated")

    assert response.status_code == 401


def test_generated_insights_is_user_isolated(client):
    token_a = register_and_login(
        client,
        "phase13_user_a@test.com",
    )

    token_b = register_and_login(
        client,
        "phase13_user_b@test.com",
    )

    response_a = client.get(
        "/api/insights/generated",
        headers={"Authorization": f"Bearer {token_a}"},
    )

    response_b = client.get(
        "/api/insights/generated",
        headers={"Authorization": f"Bearer {token_b}"},
    )

    assert response_a.status_code == 200
    assert response_b.status_code == 200

    assert response_a.json()["status"] == "success"
    assert response_b.json()["status"] == "success"

    assert response_a.json()["insights"] == []
    assert response_b.json()["insights"] == []


def test_generated_insights_with_wellbeing_history(client, db_session):
    token = register_and_login(
        client,
        "phase13_realistic@test.com",
    )

    user = db_session.query(User).filter(
        User.email == "phase13_realistic@test.com"
    ).first()

    scores = [
        WellBeingScore(
            user_id=user.id,
            score_date=date.today(),
            score=80,
        ),
        WellBeingScore(
            user_id=user.id,
            score_date=date.today().replace(day=date.today().day - 1),
            score=75,
        ),
        WellBeingScore(
            user_id=user.id,
            score_date=date.today().replace(day=date.today().day - 2),
            score=70,
        ),
    ]

    db_session.add_all(scores)
    db_session.commit()

    response = client.get(
        "/api/insights/generated",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "insights" in data
    assert "meta" in data
    assert "disclaimer" in data["meta"]

    for insight in data["insights"]:
        assert "insight_key" in insight
        assert "category" in insight
        assert "title" in insight
        assert "explanation" in insight
        assert "supporting_metrics" in insight