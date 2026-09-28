from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email():
    initial_response = client.get("/activities")
    activity_name = "Chess Club"
    email = initial_response.json()[activity_name]["participants"][0]

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    remaining = client.get("/activities").json()[activity_name]["participants"]
    assert email not in remaining


def test_unregister_missing_participant_returns_404():
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "not-signed-up@mergington.edu"},
    )

    assert response.status_code == 404
