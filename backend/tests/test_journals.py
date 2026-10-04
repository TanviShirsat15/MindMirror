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

def test_multiple_same_date_and_multiline_content(client):
    token = register_and_login(
        client,
        "same_date_journal_test@mindmirror.com",
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    multiline_content = "First paragraph.\n\nSecond paragraph.\nThird line."

    response = client.post(
        "/api/journals",
        headers=headers,
        json={
            "content": "One sentence journal entry.",
            "entry_date": "2026-10-03",
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/api/journals",
        headers=headers,
        json={
            "content": multiline_content,
            "entry_date": "2026-10-03",
        },
    )

    assert response.status_code == 201

    entries = client.get(
        "/api/journals",
        headers=headers,
    )

    assert entries.status_code == 200

    journal_entries = entries.json()

    assert len(journal_entries) == 2
    assert any(
        entry["content"] == "One sentence journal entry."
        for entry in journal_entries
    )
    assert any(
        entry["content"] == multiline_content
        for entry in journal_entries
    )


def test_unauthenticated_journal_access_is_rejected(client):
    response = client.get("/api/journals")

    assert response.status_code == 401


def test_journal_cross_user_isolation(client):
    token_a = register_and_login(
        client,
        "journal_owner_a@mindmirror.com",
    )

    headers_a = {
        "Authorization": f"Bearer {token_a}"
    }

    response = client.post(
        "/api/journals",
        headers=headers_a,
        json={
            "content": "Private journal belonging to User A.",
            "entry_date": "2026-10-03",
        },
    )

    assert response.status_code == 201

    journal_id = response.json()["id"]

    token_b = register_and_login(
        client,
        "journal_owner_b@mindmirror.com",
    )

    headers_b = {
        "Authorization": f"Bearer {token_b}"
    }

    response = client.get(
        f"/api/journals/{journal_id}",
        headers=headers_b,
    )

    assert response.status_code == 404

    response = client.put(
        f"/api/journals/{journal_id}",
        headers=headers_b,
        json={
            "content": "User B should not be able to edit this.",
        },
    )

    assert response.status_code == 404

    response = client.delete(
        f"/api/journals/{journal_id}",
        headers=headers_b,
    )

    assert response.status_code == 404

    response = client.get(
        f"/api/journals/{journal_id}",
        headers=headers_a,
    )

    assert response.status_code == 200
    assert response.json()["content"] == "Private journal belonging to User A."