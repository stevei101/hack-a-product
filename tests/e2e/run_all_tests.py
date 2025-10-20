#!/usr/bin/env python3
"""
Complete E2E test suite runner
"""
import sys
import os
import time
import requests
from typing import List, Tuple

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from tests.e2e.test_api_keys import run_api_key_tests
from tests.e2e.test_agents import run_agent_tests
from tests.e2e.test_nim_integration import run_nim_tests


class E2ETestRunner:
    """Complete E2E test runner"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        self.test_results: List[Tuple[str, bool, str]] = []
    
    def wait_for_services(self, timeout: int = 60) -> bool:
        """Wait for services to be ready"""
        print("⏳ Waiting for services to start...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Check backend health
                backend_response = requests.get(f"{self.base_url}/health", timeout=5)
                if backend_response.status_code == 200:
                    print("✅ Backend is ready")
                    
                    # Check frontend (optional)
                    try:
                        frontend_response = requests.get(self.frontend_url, timeout=5)
                        if frontend_response.status_code == 200:
                            print("✅ Frontend is ready")
                    except requests.RequestException:
                        print("⚠️  Frontend not available (optional for API tests)")
                    
                    return True
            except requests.RequestException:
                pass
            
            time.sleep(2)
        
        print("❌ Services did not start within timeout")
        return False
    
    def run_test_suite(self, test_name: str, test_function) -> bool:
        """Run a specific test suite"""
        print(f"\n🧪 Running {test_name}...")
        print("=" * 50)
        
        try:
            success = test_function()
            self.test_results.append((test_name, success, "PASSED" if success else "FAILED"))
            return success
        except Exception as e:
            error_msg = f"Test suite failed with exception: {str(e)}"
            print(f"❌ {error_msg}")
            self.test_results.append((test_name, False, error_msg))
            return False
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("📊 E2E TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for _, success, _ in self.test_results if success)
        failed_tests = total_tests - passed_tests
        
        for test_name, success, message in self.test_results:
            status_icon = "✅" if success else "❌"
            print(f"{status_icon} {test_name}: {message}")
        
        print("\n" + "-" * 60)
        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests == 0:
            print("\n🎉 All E2E tests passed! Your application is ready for production.")
        else:
            print(f"\n⚠️  {failed_tests} test suite(s) failed. Please review the errors above.")
        
        return failed_tests == 0
    
    def run_all_tests(self) -> bool:
        """Run the complete E2E test suite"""
        print("🚀 Starting Complete E2E Test Suite")
        print("=" * 60)
        
        # Wait for services to be ready
        if not self.wait_for_services():
            print("❌ Services are not ready. Please start the backend and frontend.")
            return False
        
        # Define test suites
        test_suites = [
            ("API Key Management", run_api_key_tests),
            ("Agent Management", run_agent_tests),
            ("NVIDIA NIM Integration", run_nim_tests),
        ]
        
        # Run all test suites
        for test_name, test_function in test_suites:
            self.run_test_suite(test_name, test_function)
        
        # Print summary
        return self.print_summary()


def main():
    """Main entry point"""
    runner = E2ETestRunner()
    success = runner.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
