def test_dashboard_summary(test_client, auth_headers):
    res = test_client.get("/api/dashboard/summary", headers=auth_headers)
    assert res.status_code == 200

    data = res.json()
    assert "total_income" in data
    assert "total_expenses" in data
    assert "net_balance" in data
    assert "savings_rate" in data


def test_recent_transactions(test_client, auth_headers):
    res = test_client.get("/api/dashboard/recent-transactions", headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
