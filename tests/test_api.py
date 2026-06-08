import copy
import urllib.parse
import pytest
from fastapi.testclient import TestClient
from src import app as app_module

client = TestClient(app_module.app)


@pytest.fixture(autouse=True)
def restore_activities():
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)


def test_root_redirect():
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code in (307, 308)
    assert resp.headers.get("location") == "/static/index.html"


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_for_activity():
    activity_name = "Chess Club"
    email = "tester@example.com"
    encoded = urllib.parse.quote(activity_name, safe="")
    resp = client.post(f"/activities/{encoded}/signup", params={"email": email})
    assert resp.status_code == 200
    json_resp = resp.json()
    assert f"Signed up {email} for {activity_name}" in json_resp.get("message", "")
    assert email in app_module.activities[activity_name]["participants"]
