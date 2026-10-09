from datetime import date, timedelta

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

def test_habit_complete_and_undo(client):
    token = register_and_login(
        client,
        "habit_complete_user@mindmirror.com",
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create habit
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

    habit_id = response.json()["id"]

    # Complete habit
    response = client.post(
        f"/api/habits/{habit_id}/complete",
        headers=headers,
        params={
            "log_date": "2026-10-04",
        },
    )

    assert response.status_code == 200

    log = response.json()

    assert log["habit_id"] == habit_id
    assert log["log_date"] == "2026-10-04"
    assert log["is_completed"] is True

    log_id = log["id"]

    # Complete again on the same date.
    # It should update the existing row instead of creating another row.
    response = client.post(
        f"/api/habits/{habit_id}/complete",
        headers=headers,
        params={
            "log_date": "2026-10-04",
        },
    )

    assert response.status_code == 200
    assert response.json()["id"] == log_id

    # Undo habit
    response = client.post(
        f"/api/habits/{habit_id}/undo",
        headers=headers,
        params={
            "log_date": "2026-10-04",
        },
    )

    assert response.status_code == 200

    undone_log = response.json()

    assert undone_log["id"] == log_id
    assert undone_log["is_completed"] is False

    # Verify the row still exists
    response = client.get(
        f"/api/habit-logs/{habit_id}",
        headers=headers,
    )

    assert response.status_code == 200

    logs = response.json()

    assert len(logs) == 1
    assert logs[0]["id"] == log_id
    assert logs[0]["is_completed"] is False

def test_habit_metrics(client):
    token = register_and_login(
        client,
        "habit_metrics_user@mindmirror.com",
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create habit
    response = client.post(
        "/api/habits",
        headers=headers,
        json={
            "name": "Reading",
            "target_value": 30,
            "target_unit": "minutes",
            "frequency": "daily",
        },
    )

    assert response.status_code == 201
    habit_id = response.json()["id"]

    # Complete three consecutive days before today
    today = date.today()
    log_dates = [
        today - timedelta(days=3),
        today - timedelta(days=2),
        today - timedelta(days=1),
    ]

    for log_date in log_dates:
        response = client.post(
            f"/api/habits/{habit_id}/complete",
            headers=headers,
            params={"log_date": log_date.isoformat()},
        )
        assert response.status_code == 200

    # Weekly metrics
    response = client.get(
        f"/api/habits/{habit_id}/metrics",
        headers=headers,
        params={"window": "weekly"},
    )

    assert response.status_code == 200
    metrics = response.json()

    assert metrics["window"] == "weekly"
    assert metrics["completed_days"] == 3
    assert metrics["expected_days"] == 7
    assert metrics["completion_rate"] == 42.86
    assert metrics["current_streak"] == 3
    assert metrics["longest_streak"] == 3

    # Historical metrics
    response = client.get(
        f"/api/habits/{habit_id}/metrics",
        headers=headers,
        params={"window": "historical"},
    )

    assert response.status_code == 200
    historical = response.json()

    assert historical["window"] == "historical"
    assert historical["completed_days"] == 0
    assert historical["longest_streak"] == 0


def test_habit_cross_user_isolation(client):
    token_a = register_and_login(
        client,
        "habit_owner_a@mindmirror.com",
    )

    token_b = register_and_login(
        client,
        "habit_owner_b@mindmirror.com",
    )

    headers_a = {
        "Authorization": f"Bearer {token_a}"
    }

    headers_b = {
        "Authorization": f"Bearer {token_b}"
    }

    # User A creates a habit
    response = client.post(
        "/api/habits",
        headers=headers_a,
        json={
            "name": "Private Habit",
            "target_value": 1,
            "target_unit": "time",
            "frequency": "daily",
        },
    )

    assert response.status_code == 201

    habit_id = response.json()["id"]

    # User B cannot read User A's habit
    response = client.get(
        f"/api/habits/{habit_id}",
        headers=headers_b,
    )

    assert response.status_code == 404

    # User B cannot update User A's habit
    response = client.put(
        f"/api/habits/{habit_id}",
        headers=headers_b,
        json={
            "name": "Hacked Habit",
        },
    )

    assert response.status_code == 404

    # User B cannot delete User A's habit
    response = client.delete(
        f"/api/habits/{habit_id}",
        headers=headers_b,
    )

    assert response.status_code == 404

def test_habit_completion_cross_user_isolation(client):
    token_a = register_and_login(
        client,
        "habit_complete_owner_a@mindmirror.com",
    )

    token_b = register_and_login(
        client,
        "habit_complete_owner_b@mindmirror.com",
    )

    headers_a = {
        "Authorization": f"Bearer {token_a}"
    }

    headers_b = {
        "Authorization": f"Bearer {token_b}"
    }

    # User A creates a habit
    response = client.post(
        "/api/habits",
        headers=headers_a,
        json={
            "name": "Private Exercise",
            "target_value": 30,
            "target_unit": "minutes",
            "frequency": "daily",
        },
    )

    assert response.status_code == 201

    habit_id = response.json()["id"]

    # User B cannot complete User A's habit
    response = client.post(
        f"/api/habits/{habit_id}/complete",
        headers=headers_b,
        params={"log_date": "2026-10-04"},
    )

    assert response.status_code == 404

    # User B cannot undo User A's habit
    response = client.post(
        f"/api/habits/{habit_id}/undo",
        headers=headers_b,
        params={"log_date": "2026-10-04"},
    )

    assert response.status_code == 404

def test_habit_logs_and_metrics_cross_user_isolation(client):
    token_a = register_and_login(
        client,
        "habit_data_owner_a@mindmirror.com",
    )

    token_b = register_and_login(
        client,
        "habit_data_owner_b@mindmirror.com",
    )

    headers_a = {
        "Authorization": f"Bearer {token_a}"
    }

    headers_b = {
        "Authorization": f"Bearer {token_b}"
    }

    # User A creates a habit
    response = client.post(
        "/api/habits",
        headers=headers_a,
        json={
            "name": "Private Reading",
            "target_value": 30,
            "target_unit": "minutes",
            "frequency": "daily",
        },
    )

    assert response.status_code == 201

    habit_id = response.json()["id"]

    # User A creates a completed log
    response = client.post(
        f"/api/habits/{habit_id}/complete",
        headers=headers_a,
        params={"log_date": "2026-10-04"},
    )

    assert response.status_code == 200

    # User B cannot read User A's logs
    response = client.get(
        f"/api/habit-logs/{habit_id}",
        headers=headers_b,
    )

    assert response.status_code == 404

    # User B cannot read User A's metrics
    response = client.get(
        f"/api/habits/{habit_id}/metrics",
        headers=headers_b,
        params={"window": "weekly"},
    )

    assert response.status_code == 404

def test_habit_deactivate_preserves_history(client):
    token = register_and_login(
        client,
        "habit_deactivate_user@mindmirror.com",
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create habit
    response = client.post(
        "/api/habits",
        headers=headers,
        json={
            "name": "Meditation",
            "target_value": 20,
            "target_unit": "minutes",
            "frequency": "daily",
        },
    )

    assert response.status_code == 201

    habit_id = response.json()["id"]

    # Create a completed log
    response = client.post(
        f"/api/habits/{habit_id}/complete",
        headers=headers,
        params={"log_date": "2026-10-04"},
    )

    assert response.status_code == 200

    # Deactivate habit
    response = client.put(
        f"/api/habits/{habit_id}",
        headers=headers,
        json={
            "is_active": False,
        },
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False

    # Habit should still exist
    response = client.get(
        f"/api/habits/{habit_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False

    # Historical log should still exist
    response = client.get(
        f"/api/habit-logs/{habit_id}",
        headers=headers,
    )

    assert response.status_code == 200

    logs = response.json()

    assert len(logs) == 1
    assert logs[0]["is_completed"] is True

def test_habit_hard_delete_cascades_logs(client):
    token = register_and_login(
        client,
        "habit_delete_user@mindmirror.com",
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create habit
    response = client.post(
        "/api/habits",
        headers=headers,
        json={
            "name": "Temporary Habit",
            "target_value": 1,
            "target_unit": "time",
            "frequency": "daily",
        },
    )

    assert response.status_code == 201

    habit_id = response.json()["id"]

    # Create a completed log
    response = client.post(
        f"/api/habits/{habit_id}/complete",
        headers=headers,
        params={"log_date": "2026-10-04"},
    )

    assert response.status_code == 200

    # Confirm log exists
    response = client.get(
        f"/api/habit-logs/{habit_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1

    # Hard delete the habit
    response = client.delete(
        f"/api/habits/{habit_id}",
        headers=headers,
    )

    assert response.status_code == 204

    # Habit should no longer exist
    response = client.get(
        f"/api/habits/{habit_id}",
        headers=headers,
    )

    assert response.status_code == 404

    # Its logs should also be gone
    response = client.get(
        f"/api/habit-logs/{habit_id}",
        headers=headers,
    )

    assert response.status_code == 404

def test_habit_validation(client):
    token = register_and_login(
        client,
        "habit_validation_user@mindmirror.com",
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Empty name
    response = client.post(
        "/api/habits",
        headers=headers,
        json={
            "name": "   ",
            "target_value": 1,
            "target_unit": "time",
            "frequency": "daily",
        },
    )

    assert response.status_code == 422

    # Zero target
    response = client.post(
        "/api/habits",
        headers=headers,
        json={
            "name": "Reading",
            "target_value": 0,
            "target_unit": "minutes",
            "frequency": "daily",
        },
    )

    assert response.status_code == 422

    # Negative target
    response = client.post(
        "/api/habits",
        headers=headers,
        json={
            "name": "Reading",
            "target_value": -5,
            "target_unit": "minutes",
            "frequency": "daily",
        },
    )

    assert response.status_code == 422

    # Unsupported frequency
    response = client.post(
        "/api/habits",
        headers=headers,
        json={
            "name": "Reading",
            "target_value": 30,
            "target_unit": "minutes",
            "frequency": "weekly",
        },
    )

    assert response.status_code == 422

def test_habit_persistence(client):
    token = register_and_login(
        client,
        "habit_persistence_user@mindmirror.com",
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create custom habit
    response = client.post(
        "/api/habits",
        headers=headers,
        json={
            "name": "Daily Coding",
            "target_value": 2,
            "target_unit": "hours",
            "frequency": "daily",
        },
    )

    assert response.status_code == 201

    habit = response.json()
    habit_id = habit["id"]

    assert habit["name"] == "Daily Coding"
    assert float(habit["target_value"]) == 2
    assert habit["target_unit"] == "hours"
    assert habit["frequency"] == "daily"

    # Create completion
    response = client.post(
        f"/api/habits/{habit_id}/complete",
        headers=headers,
        params={"log_date": "2026-10-04"},
    )

    assert response.status_code == 200

    # Fetch habits again
    response = client.get(
        "/api/habits",
        headers=headers,
    )

    assert response.status_code == 200

    habits = response.json()

    saved_habit = next(
        habit for habit in habits
        if habit["id"] == habit_id
    )

    assert saved_habit["name"] == "Daily Coding"
    assert float(saved_habit["target_value"]) == 2
    assert saved_habit["target_unit"] == "hours"
    assert saved_habit["frequency"] == "daily"

    # Fetch logs again
    response = client.get(
        f"/api/habit-logs/{habit_id}",
        headers=headers,
    )

    assert response.status_code == 200

    logs = response.json()

    assert len(logs) == 1
    assert logs[0]["log_date"] == "2026-10-04"
    assert logs[0]["is_completed"] is True