def register_and_login(client, email, password="TestPassword123!"):
    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Journal Test User",
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


def test_journal_crud_and_unlimited_content(client):
    token = register_and_login(
        client,
        "journal_test_user@mindmirror.com",
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    long_content = (
        "This is a journal entry. " * 500
        + "\nThis is another paragraph."
    )

    # Create journal with content well beyond 1000 words/characters.
    response = client.post(
        "/api/journals",
        headers=headers,
        json={
            "content": long_content,
            "entry_date": "2026-10-03",
        },
    )

    assert response.status_code == 201

    journal = response.json()

    assert journal["content"] == long_content
    journal_id = journal["id"]

    # Read
    response = client.get(
        f"/api/journals/{journal_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["content"] == long_content

    # Update
    updated_content = "Updated journal entry."

    response = client.put(
        f"/api/journals/{journal_id}",
        headers=headers,
        json={
            "content": updated_content,
        },
    )

    assert response.status_code == 200
    assert response.json()["content"] == updated_content

    # List
    response = client.get(
        "/api/journals",
        headers=headers,
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1

    # Delete
    response = client.delete(
        f"/api/journals/{journal_id}",
        headers=headers,
    )

    assert response.status_code == 204

    # Confirm it no longer exists
    response = client.get(
        f"/api/journals/{journal_id}",
        headers=headers,
    )

    assert response.status_code == 404


def test_empty_journal_is_rejected(client):
    token = register_and_login(
        client,
        "empty_journal_test@mindmirror.com",
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post(
        "/api/journals",
        headers=headers,
        json={
            "content": "   ",
            "entry_date": "2026-10-03",
        },
    )

    assert response.status_code == 422