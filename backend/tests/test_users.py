def test_get_me(test_client, auth_headers):
    res = test_client.get("/api/users/me", headers=auth_headers)
    assert res.status_code == 200
    assert "username" in res.json()
