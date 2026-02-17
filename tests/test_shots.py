def _create_shot(client):
    """Helper to create a show → sequence → shot chain."""
    show = client.post("/shows", json={"title": "Shot Test", "code": "SHT"}).json()
    seq = client.post(
        "/sequences",
        json={"show_id": show["id"], "code": "SEQ"},
    ).json()
    shot = client.post(
        "/shots",
        json={"sequence_id": seq["id"], "code": "SEQ_0010"},
    ).json()
    return shot


def test_create_shot(client):
    shot = _create_shot(client)
    assert shot["code"] == "SEQ_0010"
    assert shot["status"] == "pending"
    assert shot["frame_start"] == 1001


def test_list_shots_filter_status(client):
    shot = _create_shot(client)
    # Update to review status
    client.patch(f"/shots/{shot['id']}", json={"status": "review"})

    resp = client.get("/shots?status=review")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["status"] == "review"

    resp = client.get("/shots?status=approved")
    assert resp.status_code == 200
    assert len(resp.json()) == 0


def test_update_shot(client):
    shot = _create_shot(client)
    resp = client.patch(
        f"/shots/{shot['id']}",
        json={"status": "in_progress", "assigned_to": "Test Artist"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "in_progress"
    assert data["assigned_to"] == "Test Artist"


def test_get_shot_detail(client):
    shot = _create_shot(client)
    resp = client.get(f"/shots/{shot['id']}")
    assert resp.status_code == 200
    data = resp.json()
    assert "reviews" in data


def test_update_shot_not_found(client):
    resp = client.patch("/shots/999", json={"status": "review"})
    assert resp.status_code == 404
