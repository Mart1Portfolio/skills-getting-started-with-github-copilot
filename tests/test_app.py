import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

TEST_ACTIVITY = "Chess Club"
TEST_EMAIL = "test_student@example.com"


def setup_function():
    # Ensure test email not present before each test
    if TEST_EMAIL in activities[TEST_ACTIVITY]["participants"]:
        activities[TEST_ACTIVITY]["participants"].remove(TEST_EMAIL)


def teardown_function():
    # Clean up after tests
    if TEST_EMAIL in activities[TEST_ACTIVITY]["participants"]:
        activities[TEST_ACTIVITY]["participants"].remove(TEST_EMAIL)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert TEST_ACTIVITY in data
    assert "description" in data[TEST_ACTIVITY]


def test_signup_and_duplicate_prevention():
    # Sign up successfully
    resp = client.post(f"/activities/{TEST_ACTIVITY}/signup", params={"email": TEST_EMAIL})
    assert resp.status_code == 200
    assert TEST_EMAIL in activities[TEST_ACTIVITY]["participants"]

    # Duplicate signup should be rejected
    dup = client.post(f"/activities/{TEST_ACTIVITY}/signup", params={"email": TEST_EMAIL})
    assert dup.status_code == 400


def test_unregister_participant():
    # Ensure participant present
    if TEST_EMAIL not in activities[TEST_ACTIVITY]["participants"]:
        client.post(f"/activities/{TEST_ACTIVITY}/signup", params={"email": TEST_EMAIL})

    # Delete participant
    resp = client.delete(f"/activities/{TEST_ACTIVITY}/signup", params={"email": TEST_EMAIL})
    assert resp.status_code == 200
    assert TEST_EMAIL not in activities[TEST_ACTIVITY]["participants"]
