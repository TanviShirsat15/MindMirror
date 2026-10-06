from datetime import date


TEST_DATE = date.today().isoformat()


def register_and_login(client, email):
    password = "TestPassword123!"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Wellbeing Test User",
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

    return response.json()["access_token"]


def create_habit(client, headers):
    response = client.post(
        "/api/habits",
        headers=headers,
        json={
            "name": "Exercise",
            "target_value": 30,
            "target_unit": "minutes",
            "frequency": "daily",
        },
    )

    assert response.status_code == 201
    return response.json()["id"]


def create_journal(client, headers, entry_date=TEST_DATE):
    response = client.post(
        "/api/journals",
        headers=headers,
        json={
            "content": "I feel happy and calm today.",
            "entry_date": entry_date,
        },
    )

    assert response.status_code == 201
    return response.json()["id"]


def test_journal_creates_wellbeing_score(client):
    token = register_and_login(
        client,
        "wellbeing_create@mindmirror.com",
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    create_habit(client, headers)
    create_journal(client, headers)

    response = client.get(
        f"/api/wellbeing/{TEST_DATE}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["date"] == TEST_DATE
    assert 1 <= data["score"] <= 100


def test_missing_wellbeing_score_returns_404(client):
    token = register_and_login(
        client,
        "wellbeing_missing@mindmirror.com",
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get(
        f"/api/wellbeing/{TEST_DATE}",
        headers=headers,
    )

    assert response.status_code == 404


def test_habit_completion_changes_wellbeing_score(client):
    token = register_and_login(
        client,
        "wellbeing_habit@mindmirror.com",
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    habit_id = create_habit(client, headers)
    create_journal(client, headers)

    response = client.get(
        f"/api/wellbeing/{TEST_DATE}",
        headers=headers,
    )

    assert response.status_code == 200
    score_before = response.json()["score"]

    response = client.post(
        f"/api/habits/{habit_id}/complete",
        headers=headers,
        params={
            "log_date": TEST_DATE,
        },
    )

    assert response.status_code == 200

    response = client.get(
        f"/api/wellbeing/{TEST_DATE}",
        headers=headers,
    )

    assert response.status_code == 200
    score_after = response.json()["score"]

    assert score_after > score_before

    response = client.post(
        f"/api/habits/{habit_id}/undo",
        headers=headers,
        params={
            "log_date": TEST_DATE,
        },
    )

    assert response.status_code == 200

    response = client.get(
        f"/api/wellbeing/{TEST_DATE}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["score"] == score_before


def test_deleting_last_journal_removes_wellbeing_score(client):
    token = register_and_login(
        client,
        "wellbeing_delete@mindmirror.com",
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    create_habit(client, headers)
    journal_id = create_journal(client, headers)

    response = client.get(
        f"/api/wellbeing/{TEST_DATE}",
        headers=headers,
    )

    assert response.status_code == 200

    response = client.delete(
        f"/api/journals/{journal_id}",
        headers=headers,
    )

    assert response.status_code == 204

    response = client.get(
        f"/api/wellbeing/{TEST_DATE}",
        headers=headers,
    )

    assert response.status_code == 404


def test_wellbeing_score_is_user_isolated(client):
    token_a = register_and_login(
        client,
        "wellbeing_user_a@mindmirror.com",
    )

    headers_a = {
        "Authorization": f"Bearer {token_a}"
    }

    create_habit(client, headers_a)
    create_journal(client, headers_a)

    response = client.get(
        f"/api/wellbeing/{TEST_DATE}",
        headers=headers_a,
    )

    assert response.status_code == 200

    token_b = register_and_login(
        client,
        "wellbeing_user_b@mindmirror.com",
    )

    headers_b = {
        "Authorization": f"Bearer {token_b}"
    }

    response = client.get(
        f"/api/wellbeing/{TEST_DATE}",
        headers=headers_b,
    )

    assert response.status_code == 404