"""
End-to-end tests for Agent management
"""
import requests
import json
from typing import Dict, Any


class TestAgents:
    """Test agent management functionality"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.api_url = f"{self.base_url}/api/v1"
        self.api_key = None
        self.test_agent_id = None
    
    def setup_method(self):
        """Setup for each test method"""
        self.api_key = self._get_test_api_key()
    
    def _get_test_api_key(self) -> str:
        """Get API key for testing"""
        return "test-api-key"  # This needs to be replaced with actual API key
    
    def _make_request(self, method: str, endpoint: str, data: Dict[Any, Any] = None) -> requests.Response:
        """Make authenticated API request"""
        url = f"{self.api_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
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
    
    def test_create_agent(self):
        """Test creating a new agent"""
        agent_data = {
            "name": "Test Agent",
            "description": "A test agent for E2E testing",
            "capabilities": ["reasoning", "task_execution"],
            "status": "active",
            "config": {
                "max_tasks": 10,
                "timeout": 300
            }
        }
        
        response = self._make_request("POST", "/agents", data=agent_data)
        
        assert response.status_code == 201
        data = response.json()
        
        # Verify response structure
        assert "id" in data
        assert data["name"] == agent_data["name"]
        assert data["description"] == agent_data["description"]
        assert data["status"] == agent_data["status"]
        
        # Store agent ID for other tests
        self.test_agent_id = data["id"]
        
        return data
    
    def test_list_agents(self):
        """Test listing agents"""
        response = self._make_request("GET", "/agents")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "agents" in data
        assert "total" in data
        assert isinstance(data["agents"], list)
    
    def test_get_agent(self):
        """Test getting a specific agent"""
        if not self.test_agent_id:
            self.test_create_agent()
        
        response = self._make_request("GET", f"/agents/{self.test_agent_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == self.test_agent_id
        assert "name" in data
        assert "status" in data
    
    def test_update_agent(self):
        """Test updating an agent"""
        if not self.test_agent_id:
            self.test_create_agent()
        
        update_data = {
            "name": "Updated Test Agent",
            "status": "inactive"
        }
        
        response = self._make_request("PUT", f"/agents/{self.test_agent_id}", data=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == update_data["name"]
        assert data["status"] == update_data["status"]
    
    def test_agent_status_update(self):
        """Test updating agent status"""
        if not self.test_agent_id:
            self.test_create_agent()
        
        status_data = {"status": "busy"}
        
        response = self._make_request("PUT", f"/agents/{self.test_agent_id}/status", data=status_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == status_data["status"]


def run_agent_tests():
    """Run all agent tests"""
    test_instance = TestAgents()
    test_instance.setup_method()
    
    print("🤖 Running Agent E2E Tests...")
    
    try:
        print("✅ Testing agent creation...")
        test_instance.test_create_agent()
        
        print("✅ Testing agent listing...")
        test_instance.test_list_agents()
        
        print("✅ Testing agent retrieval...")
        test_instance.test_get_agent()
        
        print("✅ Testing agent update...")
        test_instance.test_update_agent()
        
        print("✅ Testing agent status update...")
        test_instance.test_agent_status_update()
        
        print("🎉 All Agent E2E tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Agent E2E test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_agent_tests()
    exit(0 if success else 1)
