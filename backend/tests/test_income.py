def test_create_income(test_client, auth_headers):
    res = test_client.post("/api/income", json={
        "source": "Salary",
        "amount": 5000,
        "date": "2026-01-01T00:00:00",
        "category": "Job"
    }, headers=auth_headers)

    assert res.status_code == 200
    assert res.json()["source"] == "Salary"


def test_get_income(test_client, auth_headers):
    res = test_client.get("/api/income", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
