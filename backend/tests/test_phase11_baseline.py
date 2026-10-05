def register_and_login(client, email):
    password = "TestPassword123!"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Baseline Test User",
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


def create_score(client, headers, score_date, score):
    response = client.post(
        "/api/wellbeing-scores",
        headers=headers,
        json={
            "score_date": score_date,
            "score": score,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_first_score_has_insufficient_history(client):
    token = register_and_login(
        client,
        "baseline_first@mindmirror.com",
    )
    headers = {"Authorization": f"Bearer {token}"}

    create_score(client, headers, "2026-10-01", 70)

    response = client.get(
        "/api/wellbeing/2026-10-01",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "insufficient_history"
    assert data["baseline"] is None
    assert data["difference"] is None
    assert data["comparison"] is None
    assert data["baseline_sample_size"] == 0


def test_two_previous_scores_are_insufficient(client):
    token = register_and_login(
        client,
        "baseline_two@mindmirror.com",
    )
    headers = {"Authorization": f"Bearer {token}"}

    create_score(client, headers, "2026-10-01", 60)
    create_score(client, headers, "2026-10-02", 70)
    create_score(client, headers, "2026-10-03", 80)

    response = client.get(
        "/api/wellbeing/2026-10-03",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "insufficient_history"
    assert data["baseline"] is None
    assert data["baseline_sample_size"] == 2


def test_exactly_three_previous_scores_create_baseline(client):
    token = register_and_login(
        client,
        "baseline_three@mindmirror.com",
    )
    headers = {"Authorization": f"Bearer {token}"}

    create_score(client, headers, "2026-10-01", 60)
    create_score(client, headers, "2026-10-02", 70)
    create_score(client, headers, "2026-10-03", 80)
    create_score(client, headers, "2026-10-04", 90)

    response = client.get(
        "/api/wellbeing/2026-10-04",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "baseline_available"
    assert data["baseline"] == 70.0
    assert data["baseline_sample_size"] == 3
    assert data["difference"] == 20.0
    assert data["comparison"] == "above"


def test_current_score_is_excluded_from_baseline(client):
    token = register_and_login(
        client,
        "baseline_current@mindmirror.com",
    )
    headers = {"Authorization": f"Bearer {token}"}

    create_score(client, headers, "2026-10-01", 60)
    create_score(client, headers, "2026-10-02", 70)
    create_score(client, headers, "2026-10-03", 80)
    create_score(client, headers, "2026-10-04", 100)

    response = client.get(
        "/api/wellbeing/2026-10-04",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["baseline"] == 70.0
    assert data["baseline_sample_size"] == 3


def test_baseline_uses_recent_seven_scores(client):
    token = register_and_login(
        client,
        "baseline_seven@mindmirror.com",
    )
    headers = {"Authorization": f"Bearer {token}"}

    for day, score in enumerate([10, 20, 30, 40, 50, 60, 70, 80], start=1):
        create_score(
            client,
            headers,
            f"2026-09-{day:02d}",
            score,
        )

    create_score(client, headers, "2026-10-01", 90)

    response = client.get(
        "/api/wellbeing/2026-10-01",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "baseline_available"
    assert data["baseline_sample_size"] == 7
    assert data["baseline"] == 50.0


def test_near_boundary_is_near(client):
    token = register_and_login(
        client,
        "baseline_near@mindmirror.com",
    )
    headers = {"Authorization": f"Bearer {token}"}

    create_score(client, headers, "2026-10-01", 60)
    create_score(client, headers, "2026-10-02", 60)
    create_score(client, headers, "2026-10-03", 60)
    create_score(client, headers, "2026-10-04", 65)

    response = client.get(
        "/api/wellbeing/2026-10-04",
        headers=headers,
    )

    data = response.json()

    assert data["baseline"] == 60.0
    assert data["difference"] == 5.0
    assert data["comparison"] == "near"


def test_above_and_below_thresholds(client):
    token = register_and_login(
        client,
        "baseline_thresholds@mindmirror.com",
    )
    headers = {"Authorization": f"Bearer {token}"}

    create_score(client, headers, "2026-10-01", 60)
    create_score(client, headers, "2026-10-02", 60)
    create_score(client, headers, "2026-10-03", 60)

    create_score(client, headers, "2026-10-04", 66)

    response = client.get(
        "/api/wellbeing/2026-10-04",
        headers=headers,
    )

    assert response.json()["comparison"] == "above"

    create_score(client, headers, "2026-10-05", 54)

    response = client.get(
        "/api/wellbeing/2026-10-05",
        headers=headers,
    )

    assert response.json()["comparison"] == "below"


def test_cross_user_baseline_isolation(client):
    token_a = register_and_login(
        client,
        "baseline_isolation_a@mindmirror.com",
    )
    headers_a = {"Authorization": f"Bearer {token_a}"}

    create_score(client, headers_a, "2026-10-01", 90)
    create_score(client, headers_a, "2026-10-02", 90)
    create_score(client, headers_a, "2026-10-03", 90)
    create_score(client, headers_a, "2026-10-04", 90)

    token_b = register_and_login(
        client,
        "baseline_isolation_b@mindmirror.com",
    )
    headers_b = {"Authorization": f"Bearer {token_b}"}

    create_score(client, headers_b, "2026-10-04", 50)

    response = client.get(
        "/api/wellbeing/2026-10-04",
        headers=headers_b,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "insufficient_history"
    assert data["baseline"] is None
    assert data["baseline_sample_size"] == 0
