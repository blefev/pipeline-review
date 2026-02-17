def _create_shot(client):
    """Helper to create a show → sequence → shot chain."""
    show = client.post("/shows", json={"title": "Review Test", "code": "RVW"}).json()
    seq = client.post(
        "/sequences",
        json={"show_id": show["id"], "code": "SEQ"},
    ).json()
    shot = client.post(
        "/shots",
        json={"sequence_id": seq["id"], "code": "SEQ_0010"},
    ).json()
    return shot


def test_create_review(client):
    shot = _create_shot(client)
    resp = client.post(
        f"/shots/{shot['id']}/reviews",
        json={
            "author": "Joe Letteri",
            "status": "approved",
            "body": "Lighting integration looks great.",
            "department": "lighting",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["author"] == "Joe Letteri"
    assert data["status"] == "approved"
    assert data["shot_id"] == shot["id"]


def test_list_reviews(client):
    shot = _create_shot(client)
    client.post(
        f"/shots/{shot['id']}/reviews",
        json={"author": "Author A", "status": "note", "body": "First note."},
    )
    client.post(
        f"/shots/{shot['id']}/reviews",
        json={"author": "Author B", "status": "approved", "body": "Looks good."},
    )
    resp = client.get(f"/shots/{shot['id']}/reviews")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_create_review_shot_not_found(client):
    resp = client.post(
        "/shots/999/reviews",
        json={"author": "Nobody", "status": "note", "body": "No shot."},
    )
    assert resp.status_code == 404
