"""
E2E test configuration and utilities
"""
import os
from typing import Optional


class TestConfig:
    """Configuration for E2E tests"""
    
    # Service URLs
    BACKEND_URL = os.getenv("E2E_BACKEND_URL", "http://localhost:8000")
    FRONTEND_URL = os.getenv("E2E_FRONTEND_URL", "http://localhost:3000")
    
    # API Configuration
    API_V1_PREFIX = "/api/v1"
    
    # Test API Keys (these should be created during test setup)
    ADMIN_API_KEY = os.getenv("E2E_ADMIN_API_KEY", "test-admin-key")
    USER_API_KEY = os.getenv("E2E_USER_API_KEY", "test-user-key")
    READONLY_API_KEY = os.getenv("E2E_READONLY_API_KEY", "test-readonly-key")
    
    # Test Data
    TEST_AGENT_NAME = "E2E Test Agent"
    TEST_TASK_TITLE = "E2E Test Task"
    TEST_PROJECT_NAME = "E2E Test Project"
    
    # Timeouts
    REQUEST_TIMEOUT = 30
    SERVICE_STARTUP_TIMEOUT = 60
    
    # Test Settings
    VERBOSE_LOGGING = os.getenv("E2E_VERBOSE", "false").lower() == "true"
    SKIP_NIM_TESTS = os.getenv("E2E_SKIP_NIM", "false").lower() == "true"
    SKIP_AUTH_TESTS = os.getenv("E2E_SKIP_AUTH", "false").lower() == "true"


def get_test_api_key(permission_level: str = "user") -> str:
    """Get appropriate API key for testing"""
    if permission_level == "admin":
        return TestConfig.ADMIN_API_KEY
    elif permission_level == "readonly":
        return TestConfig.READONLY_API_KEY
    else:
        return TestConfig.USER_API_KEY


def should_skip_test(test_name: str) -> bool:
    """Determine if a test should be skipped based on configuration"""
    if test_name.lower().contains("nim") and TestConfig.SKIP_NIM_TESTS:
        return True
    if test_name.lower().contains("auth") and TestConfig.SKIP_AUTH_TESTS:
        return True
    return False
