def test_register(test_client):
    res = test_client.post("/api/register", json={
        "username": "user1",
        "password": "Password123!"
    })
    assert res.status_code == 200
    assert "id" in res.json()


def test_login(test_client):
    test_client.post("/api/register", json={
        "username": "user2",
        "password": "Password123!"
    })

    res = test_client.post("/api/token", data={
        "username": "user2",
        "password": "Password123!"
    })

    assert res.status_code == 200
    assert "access_token" in res.json()
