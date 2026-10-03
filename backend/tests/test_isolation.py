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

    # ---------------------------------------------------------
    # Journal
    # ---------------------------------------------------------
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

    # User A can access their own journal
    response = client.get(
        f"/api/journals/{journal_id}",
        headers=headers_a,
    )

    assert response.status_code == 200
    assert response.json()["id"] == journal_id

    # User B cannot access User A's journal
    response = client.get(
        f"/api/journals/{journal_id}",
        headers=headers_b,
    )

    assert response.status_code == 404

    # Journal analysis is read-only in the current API.
    # No analysis record can be created through an endpoint,
    # so the isolation test does not fabricate one.

    # ---------------------------------------------------------
    # Habit
    # ---------------------------------------------------------
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

    # User A can access their own habit
    response = client.get(
        f"/api/habits/{habit_id}",
        headers=headers_a,
    )

    assert response.status_code == 200
    assert response.json()["id"] == habit_id

    # User B cannot access User A's habit
    response = client.get(
        f"/api/habits/{habit_id}",
        headers=headers_b,
    )

    assert response.status_code == 404

    # ---------------------------------------------------------
    # Habit Log
    # ---------------------------------------------------------
    response = client.post(
        f"/api/habit-logs/{habit_id}",
        headers=headers_a,
        json={
            "log_date": "2026-10-03",
            "completed_value": 1,
            "is_completed": True,
        },
    )

    assert response.status_code == 201
    habit_log_id = response.json()["id"]

    # User A can access their own habit logs
    response = client.get(
        f"/api/habit-logs/{habit_id}",
        headers=headers_a,
    )

    assert response.status_code == 200
    assert any(
        log["id"] == habit_log_id
        for log in response.json()
    )

    # User B cannot access User A's habit logs
    response = client.get(
        f"/api/habit-logs/{habit_id}",
        headers=headers_b,
    )

    assert response.status_code == 404

    # ---------------------------------------------------------
    # Well-being Score
    # ---------------------------------------------------------
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

    # User A can access their own score
    response = client.get(
        f"/api/wellbeing-scores/{score_id}",
        headers=headers_a,
    )

    assert response.status_code == 200
    assert response.json()["id"] == score_id

    # User B cannot access User A's score
    response = client.get(
        f"/api/wellbeing-scores/{score_id}",
        headers=headers_b,
    )

    assert response.status_code == 404

    # ---------------------------------------------------------
    # Insight
    # ---------------------------------------------------------
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

    # User A can access their own insight
    response = client.get(
        f"/api/insights/{insight_id}",
        headers=headers_a,
    )

    assert response.status_code == 200
    assert response.json()["id"] == insight_id

    # User B cannot access User A's insight
    response = client.get(
        f"/api/insights/{insight_id}",
        headers=headers_b,
    )

    assert response.status_code == 404