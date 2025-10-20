"""
End-to-end tests for API Key management
"""
import pytest
import requests
import json
from typing import Dict, Any


class TestAPIKeys:
    """Test API key management functionality"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.api_url = f"{self.base_url}/api/v1"
        self.admin_api_key = None
        self.test_api_key = None
    
    def setup_method(self):
        """Setup for each test method"""
        # This would be set from environment or test configuration
        self.admin_api_key = self._get_admin_api_key()
    
    def _get_admin_api_key(self) -> str:
        """Get admin API key for testing"""
        # In a real scenario, this would be from environment or test setup
        return "test-admin-key"  # This needs to be replaced with actual admin key
    
    def _make_request(self, method: str, endpoint: str, data: Dict[Any, Any] = None, 
                     api_key: str = None) -> requests.Response:
        """Make authenticated API request"""
        url = f"{self.api_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        if method.upper() == "GET":
            return requests.get(url, headers=headers)
        elif method.upper() == "POST":
            return requests.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            return requests.put(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            return requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
    
    def test_health_check(self):
        """Test basic health check"""
        response = requests.get(f"{self.base_url}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_create_api_key(self):
        """Test creating a new API key"""
        api_key_data = {
            "name": "Test API Key",
            "description": "API key for testing purposes",
            "permissions": ["read", "write"],
            "rate_limit": 1000,
            "expires_in_days": 30
        }
        
        response = self._make_request(
            "POST", 
            "/api-keys", 
            data=api_key_data, 
            api_key=self.admin_api_key
        )
        
        assert response.status_code == 201
        data = response.json()
        
        # Verify response structure
        assert "id" in data
        assert "name" in data
        assert "key" in data  # The actual API key (only shown once)
        assert "key_prefix" in data
        assert "permissions" in data
        assert "rate_limit" in data
        
        # Store the API key for other tests
        self.test_api_key = data["key"]
        
        return data
    
    def test_validate_api_key(self):
        """Test API key validation"""
        if not self.test_api_key:
            # Create a test API key first
            self.test_create_api_key()
        
        validation_data = {"api_key": self.test_api_key}
        
        response = self._make_request(
            "POST", 
            "/api-keys/validate", 
            data=validation_data
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["valid"] is True
        assert "name" in data
        assert "permissions" in data
        assert "rate_limit" in data
    
    def test_list_api_keys(self):
        """Test listing API keys"""
        response = self._make_request(
            "GET", 
            "/api-keys", 
            api_key=self.admin_api_key
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "api_keys" in data
        assert "total" in data
        assert "page" in data
        assert "per_page" in data
        assert isinstance(data["api_keys"], list)
    
    def test_get_current_api_key_info(self):
        """Test getting current API key information"""
        if not self.test_api_key:
            self.test_create_api_key()
        
        response = self._make_request(
            "GET", 
            "/api-keys/me/info", 
            api_key=self.test_api_key
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "id" in data
        assert "name" in data
        assert "key_prefix" in data
        assert "permissions" in data
    
    def test_invalid_api_key(self):
        """Test invalid API key rejection"""
        invalid_key = "invalid-api-key-12345"
        
        response = self._make_request(
            "GET", 
            "/api-keys/me/info", 
            api_key=invalid_key
        )
        
        assert response.status_code == 401
    
    def test_insufficient_permissions(self):
        """Test insufficient permissions"""
        if not self.test_api_key:
            self.test_create_api_key()
        
        # Try to access admin endpoint with non-admin key
        response = self._make_request(
            "GET", 
            "/api-keys", 
            api_key=self.test_api_key
        )
        
        assert response.status_code == 403
    
    def test_missing_authorization(self):
        """Test missing authorization header"""
        response = self._make_request("GET", "/api-keys")
        assert response.status_code == 401


def run_api_key_tests():
    """Run all API key tests"""
    test_instance = TestAPIKeys()
    test_instance.setup_method()
    
    print("🧪 Running API Key E2E Tests...")
    
    try:
        print("✅ Testing health check...")
        test_instance.test_health_check()
        
        print("✅ Testing API key creation...")
        test_instance.test_create_api_key()
        
        print("✅ Testing API key validation...")
        test_instance.test_validate_api_key()
        
        print("✅ Testing API key listing...")
        test_instance.test_list_api_keys()
        
        print("✅ Testing current API key info...")
        test_instance.test_get_current_api_key_info()
        
        print("✅ Testing invalid API key rejection...")
        test_instance.test_invalid_api_key()
        
        print("✅ Testing insufficient permissions...")
        test_instance.test_insufficient_permissions()
        
        print("✅ Testing missing authorization...")
        test_instance.test_missing_authorization()
        
        print("🎉 All API Key E2E tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ API Key E2E test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_api_key_tests()
    exit(0 if success else 1)
