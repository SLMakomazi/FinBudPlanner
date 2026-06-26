def test_create_budget(test_client, auth_headers):
    res = test_client.post("/api/budget", json={
        "category": "Food",
        "limit": 1000
    }, headers=auth_headers)

    assert res.status_code == 200
    assert res.json()["category"] == "Food"


def test_get_budgets(test_client, auth_headers):
    res = test_client.get("/api/budget", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
