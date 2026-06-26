def test_create_expense(test_client, auth_headers):
    res = test_client.post("/api/expense", json={
        "description": "Food",
        "amount": 200,
        "date": "2026-01-01T00:00:00",
        "category": "Daily"
    }, headers=auth_headers)

    assert res.status_code == 200
    assert res.json()["description"] == "Food"


def test_get_expenses(test_client, auth_headers):
    res = test_client.get("/api/expense", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
