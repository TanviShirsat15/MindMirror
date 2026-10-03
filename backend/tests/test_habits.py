def register_and_login(client, email):
    password = "TestPassword123!"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Habit Test User",
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


def test_habit_and_habit_log_crud(client):
    token = register_and_login(
        client,
        "habit_test_user@mindmirror.com",
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create habit
    response = client.post(
        "/api/habits",
        headers=headers,
        json={
            "name": "Study",
            "target_value": 2,
            "target_unit": "hours",
        },
    )

    assert response.status_code == 201

    habit = response.json()
    habit_id = habit["id"]

    assert habit["name"] == "Study"
    assert float(habit["target_value"]) == 2

    # Read habit
    response = client.get(
        f"/api/habits/{habit_id}",
        headers=headers,
    )

    assert response.status_code == 200

    # Update habit
    response = client.put(
        f"/api/habits/{habit_id}",
        headers=headers,
        json={
            "name": "Deep Study",
            "target_value": 3,
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Deep Study"

    # Create habit log
    response = client.post(
        f"/api/habit-logs/{habit_id}",
        headers=headers,
        json={
            "log_date": "2026-10-03",
            "completed_value": 2.5,
            "is_completed": True,
        },
    )

    assert response.status_code == 201

    log = response.json()
    log_id = log["id"]

    assert log["is_completed"] is True

    # Read habit logs
    response = client.get(
        f"/api/habit-logs/{habit_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1

    # Duplicate date should be rejected
    response = client.post(
        f"/api/habit-logs/{habit_id}",
        headers=headers,
        json={
            "log_date": "2026-10-03",
            "completed_value": 1,
            "is_completed": True,
        },
    )

    assert response.status_code == 409

    # Update log
    response = client.put(
        f"/api/habit-logs/{habit_id}/{log_id}",
        headers=headers,
        json={
            "completed_value": 3,
        },
    )

    assert response.status_code == 200

    # Delete log
    response = client.delete(
        f"/api/habit-logs/{habit_id}/{log_id}",
        headers=headers,
    )

    assert response.status_code == 204

    # Delete habit
    response = client.delete(
        f"/api/habits/{habit_id}",
        headers=headers,
    )

    assert response.status_code == 204


def test_habit_requires_authentication(client):
    response = client.get("/api/habits")

    assert response.status_code == 401