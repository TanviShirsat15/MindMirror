def register_and_login(client, email, full_name):
    password = "TestPassword123!"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": full_name,
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


def test_user_data_isolation(client):
    # Create User A
    token_a = register_and_login(
        client,
        "isolation_user_a@mindmirror.com",
        "User A",
    )

    # Create User B
    token_b = register_and_login(
        client,
        "isolation_user_b@mindmirror.com",
        "User B",
    )

    headers_a = {
        "Authorization": f"Bearer {token_a}"
    }

    headers_b = {
        "Authorization": f"Bearer {token_b}"
    }

    # User A creates a journal
    response = client.post(
        "/api/journals",
        headers=headers_a,
        json={
            "content": "This belongs only to User A.",
            "entry_date": "2026-10-03",
        },
    )

    assert response.status_code == 201
    journal_id = response.json()["id"]

    # User B must NOT access User A's journal
    response = client.get(
        f"/api/journals/{journal_id}",
        headers=headers_b,
    )

    assert response.status_code == 404

    # User A creates a habit
    response = client.post(
        "/api/habits",
        headers=headers_a,
        json={
            "name": "Private Habit",
            "target_value": 1,
            "target_unit": "time",
        },
    )

    assert response.status_code == 201
    habit_id = response.json()["id"]

    # User B must NOT access User A's habit
    response = client.get(
        f"/api/habits/{habit_id}",
        headers=headers_b,
    )

    assert response.status_code == 404

    # User A creates a well-being score
    response = client.post(
        "/api/wellbeing-scores",
        headers=headers_a,
        json={
            "score_date": "2026-10-03",
            "score": 75,
            "baseline_value": 70,
        },
    )

    assert response.status_code == 201
    score_id = response.json()["id"]

    # User B must NOT access User A's score
    response = client.get(
        f"/api/wellbeing-scores/{score_id}",
        headers=headers_b,
    )

    assert response.status_code == 404

    # User A creates an insight
    response = client.post(
        "/api/insights",
        headers=headers_a,
        json={
            "insight_date": "2026-10-03",
            "content": "Private insight for User A.",
        },
    )

    assert response.status_code == 201
    insight_id = response.json()["id"]

    # User B must NOT access User A's insight
    response = client.get(
        f"/api/insights/{insight_id}",
        headers=headers_b,
    )

    assert response.status_code == 404

