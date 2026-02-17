def test_create_show(client):
    resp = client.post("/shows", json={"title": "Test Show", "code": "TST"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Test Show"
    assert data["code"] == "TST"
    assert data["status"] == "active"
    assert "id" in data


def test_list_shows(client):
    client.post("/shows", json={"title": "Show A", "code": "SHA"})
    client.post("/shows", json={"title": "Show B", "code": "SHB"})
    resp = client.get("/shows")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_show(client):
    create = client.post("/shows", json={"title": "Detail Show", "code": "DTL"})
    show_id = create.json()["id"]
    resp = client.get(f"/shows/{show_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Detail Show"
    assert "sequences" in data


def test_get_show_not_found(client):
    resp = client.get("/shows/999")
    assert resp.status_code == 404
