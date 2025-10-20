"""
End-to-end tests for NVIDIA NIM integration
"""
import requests
import json
from typing import Dict, Any


class TestNIMIntegration:
    """Test NVIDIA NIM integration functionality"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.api_url = f"{self.base_url}/api/v1"
        self.api_key = None
    
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
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
    
    def test_nim_health(self):
        """Test NIM service health"""
        response = self._make_request("GET", "/nim/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "model" in data
        assert "version" in data
    
    def test_nim_chat_completion(self):
        """Test NIM chat completion"""
        chat_data = {
            "messages": [
                {"role": "user", "content": "Hello, how are you?"}
            ],
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        response = self._make_request("POST", "/nim/chat/completions", data=chat_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "choices" in data
        assert len(data["choices"]) > 0
        assert "message" in data["choices"][0]
        assert "content" in data["choices"][0]["message"]
    
    def test_nim_embeddings(self):
        """Test NIM embeddings generation"""
        embedding_data = {
            "input": ["This is a test sentence", "Another test sentence"],
            "model": models.embedding_model
        }
        
        response = self._make_request("POST", "/nim/embeddings", data=embedding_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "data" in data
        assert len(data["data"]) == 2
        assert "embedding" in data["data"][0]
        assert len(data["data"][0]["embedding"]) > 0
    
    def test_nim_model_info(self):
        """Test getting NIM model information"""
        response = self._make_request("GET", "/nim/models")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "models" in data
        assert isinstance(data["models"], list)
        assert len(data["models"]) > 0


def run_nim_tests():
    """Run all NIM integration tests"""
    test_instance = TestNIMIntegration()
    test_instance.setup_method()
    
    print("🚀 Running NVIDIA NIM Integration E2E Tests...")
    
    try:
        print("✅ Testing NIM health check...")
        test_instance.test_nim_health()
        
        print("✅ Testing NIM chat completion...")
        test_instance.test_nim_chat_completion()
        
        print("✅ Testing NIM embeddings...")
        test_instance.test_nim_embeddings()
        
        print("✅ Testing NIM model info...")
        test_instance.test_nim_model_info()
        
        print("🎉 All NVIDIA NIM E2E tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ NVIDIA NIM E2E test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_nim_tests()
    exit(0 if success else 1)
