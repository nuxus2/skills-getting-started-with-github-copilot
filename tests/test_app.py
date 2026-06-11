from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


class TestActivitiesEndpoint:
    """Tests for GET /activities"""
    
    def test_get_activities_returns_all_activities(self):
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
    
    def test_get_activities_contains_required_fields(self):
        response = client.get("/activities")
        data = response.json()
        for activity_name, activity_info in data.items():
            assert "description" in activity_info
            assert "schedule" in activity_info
            assert "max_participants" in activity_info
            assert "participants" in activity_info


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup"""
    
    def test_signup_for_activity_success(self):
        response = client.post(
            "/activities/Chess%20Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
    
    def test_signup_for_nonexistent_activity(self):
        response = client.post(
            "/activities/NonExistent/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_signup_duplicate_email(self):
        # First signup
        client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")
        # Try duplicate
        response = client.post(
            "/activities/Chess%20Club/signup?email=duplicate@mergington.edu"
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()


class TestUnregisterEndpoint:
    """Tests for DELETE /activities/{activity_name}/unregister"""
    
    def test_unregister_success(self):
        # First signup
        client.post("/activities/Gym%20Class/signup?email=unregister@mergington.edu")
        # Then unregister
        response = client.delete(
            "/activities/Gym%20Class/unregister?email=unregister@mergington.edu"
        )
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
    
    def test_unregister_not_registered(self):
        response = client.delete(
            "/activities/Chess%20Club/unregister?email=notregistered@mergington.edu"
        )
        assert response.status_code == 404
