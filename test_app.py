import pytest
import requests
from unittest.mock import Mock, patch
from app import app, get_user_gists


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestGetUserGists:
    """Test the get_user_gists function."""

    @patch('app.requests.get')
    def test_successful_gist_fetch(self, mock_get):
        """Test successful fetching of user gists."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "id": "abc123",
                "description": "Test gist",
                "public": True,
                "html_url": "https://gist.github.com/octocat/abc123",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "files": {
                    "test.txt": {"filename": "test.txt"}
                }
            }
        ]
        mock_get.return_value = mock_response

        result = get_user_gists("octocat")

        assert len(result) == 1
        assert result[0]["id"] == "abc123"
        assert result[0]["description"] == "Test gist"
        assert result[0]["files"] == ["test.txt"]

    @patch('app.requests.get')
    def test_user_not_found(self, mock_get):
        """Test handling of non-existent user."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="User 'nonexistent' not found"):
            get_user_gists("nonexistent")

    @patch('app.requests.get')
    def test_network_error(self, mock_get):
        """Test handling of network errors."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        with pytest.raises(RuntimeError, match="Error fetching gists"):
            get_user_gists("octocat")


class TestAPIEndpoints:
    """Test the API endpoints."""

    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"

    @patch('app.get_user_gists')
    def test_get_gists_success(self, mock_get_gists, client):
        """Test successful gist retrieval via API."""
        mock_get_gists.return_value = [
            {
                "id": "abc123",
                "description": "Test gist",
                "public": True,
                "html_url": "https://gist.github.com/octocat/abc123",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "files": ["test.txt"]
            }
        ]

        response = client.get("/octocat")
        assert response.status_code == 200

        data = response.get_json()
        assert data["username"] == "octocat"
        assert data["gist_count"] == 1
        assert len(data["gists"]) == 1
        assert data["gists"][0]["id"] == "abc123"

    @patch('app.get_user_gists')
    def test_get_gists_user_not_found(self, mock_get_gists, client):
        """Test API response when user is not found."""
        mock_get_gists.side_effect = ValueError("User 'nonexistent' not found")

        response = client.get("/nonexistent")
        assert response.status_code == 404

        data = response.get_json()
        assert "error" in data
        assert "not found" in data["error"].lower()

    @patch('app.get_user_gists')
    def test_get_gists_server_error(self, mock_get_gists, client):
        """Test API response when server error occurs."""
        mock_get_gists.side_effect = RuntimeError("Error fetching gists")

        response = client.get("/octocat")
        assert response.status_code == 500

        data = response.get_json()
        assert "error" in data


class TestIntegrationWithRealAPI:
    """Integration test with real GitHub API."""

    def test_octocat_gists(self, client):
        """Test fetching gists for octocat user (real API call)."""
        response = client.get("/octocat")

        assert response.status_code == 200
        data = response.get_json()

        assert data["username"] == "octocat"
        assert "gist_count" in data
        assert "gists" in data
        assert isinstance(data["gists"], list)

        if data["gist_count"] > 0:
            first_gist = data["gists"][0]
            assert "id" in first_gist
            assert "html_url" in first_gist
            assert "files" in first_gist
            assert isinstance(first_gist["files"], list)
