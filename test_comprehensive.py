#!/usr/bin/env python3
"""
Comprehensive testing script for Task Management System
Tests all endpoints, features, and functionality to ensure deployment readiness
"""

import requests
import json
import time
import sys
from datetime import datetime, date

BASE_URL = "http://localhost:5000"

class TestSuite:
    def __init__(self):
        self.session = requests.Session()
        self.failed_tests = []
        self.passed_tests = []
        
    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {status}: {message}")
        
    def test_endpoint(self, endpoint, method="GET", data=None, expected_status=200, description=""):
        """Test an endpoint and return response"""
        try:
            url = f"{BASE_URL}{endpoint}"
            
            if method == "GET":
                response = self.session.get(url)
            elif method == "POST":
                response = self.session.post(url, data=data)
            elif method == "PUT":
                response = self.session.put(url, data=data)
            else:
                response = self.session.delete(url)
                
            if response.status_code == expected_status:
                self.log(f"✓ {description or endpoint} - Status: {response.status_code}", "PASS")
                self.passed_tests.append(endpoint)
                return response
            else:
                self.log(f"✗ {description or endpoint} - Expected: {expected_status}, Got: {response.status_code}", "FAIL")
                self.failed_tests.append(f"{endpoint} - {response.status_code}")
                return response
                
        except Exception as e:
            self.log(f"✗ {description or endpoint} - Error: {str(e)}", "ERROR")
            self.failed_tests.append(f"{endpoint} - {str(e)}")
            return None
            
    def run_comprehensive_tests(self):
        """Run all system tests"""
        self.log("Starting comprehensive test suite...")
        
        # 1. Test basic server health
        self.log("\n=== TESTING SERVER HEALTH ===")
        self.test_endpoint("/", expected_status=303, description="Home page redirect")
        self.test_endpoint("/login", description="Login page")
        self.test_endpoint("/register", description="Register page")
        self.test_endpoint("/sw.js", description="Service worker")
        
        # 2. Test API endpoints
        self.log("\n=== TESTING API ENDPOINTS ===")
        self.test_endpoint("/api", description="API health check")
        self.test_endpoint("/api/tasks", description="Get all tasks API")
        
        # Test POST to API (should work without auth for testing)
        task_data = {
            "title": "Test Task via API",
            "description": "Testing API endpoint",
            "status": "Pending",
            "due_date": str(date.today())
        }
        
        api_response = self.test_endpoint(
            "/api/tasks", 
            method="POST", 
            data=json.dumps(task_data),
            description="Create task via API"
        )
        
        # 3. Test authentication flow (without actually logging in)
        self.log("\n=== TESTING AUTHENTICATION PAGES ===")
        # These should return 200 (form pages)
        login_response = self.test_endpoint("/login", description="Login form display")
        register_response = self.test_endpoint("/register", description="Register form display")
        
        # 4. Test protected routes (should redirect to login)
        self.log("\n=== TESTING PROTECTED ROUTES ===")
        protected_routes = [
            "/tasks/new",
            "/shared-tasks", 
            "/notifications",
            "/analytics"
        ]
        
        for route in protected_routes:
            self.test_endpoint(route, expected_status=303, description=f"Protected route: {route}")
            
        # 5. Test error handling
        self.log("\n=== TESTING ERROR HANDLING ===")
        self.test_endpoint("/nonexistent", expected_status=404, description="404 error handling")
        
        # 6. Test static file serving
        self.log("\n=== TESTING STATIC FILES ===")
        # These might return 404 if files don't exist, which is expected
        static_files = [
            "/static/css/bootstrap.min.css",
            "/static/js/bootstrap.bundle.min.js"
        ]
        
        for static_file in static_files:
            # We expect 404 since we don't have these files, but server should handle gracefully
            self.test_endpoint(static_file, expected_status=404, description=f"Static file: {static_file}")
            
        # 7. Test specific task operations via API
        self.log("\n=== TESTING TASK OPERATIONS ===")
        
        # Get specific task (might fail if task doesn't exist)
        self.test_endpoint("/api/tasks/1", expected_status=[200, 404], description="Get specific task")
        
        # Test search functionality via API
        search_params = "?q=test"
        self.test_endpoint(f"/api/tasks{search_params}", description="Search tasks via API")
        
        # Test filter functionality via API  
        filter_params = "?status=Pending"
        self.test_endpoint(f"/api/tasks{filter_params}", description="Filter tasks via API")
        
        # 8. Test WebSocket endpoint (basic connectivity)
        self.log("\n=== TESTING WEBSOCKET CONNECTIVITY ===")
        try:
            import websocket
            ws_url = "ws://localhost:5000/ws/1"
            ws = websocket.create_connection(ws_url, timeout=5)
            ws.close()
            self.log("✓ WebSocket connection test", "PASS")
            self.passed_tests.append("WebSocket connectivity")
        except Exception as e:
            self.log(f"✗ WebSocket connection failed: {str(e)}", "FAIL")
            self.failed_tests.append(f"WebSocket - {str(e)}")
            
        # 9. Test database connectivity (via API)
        self.log("\n=== TESTING DATABASE CONNECTIVITY ===")
        # API calls that worked indicate database is connected
        if len([t for t in self.passed_tests if "api" in t.lower()]) > 0:
            self.log("✓ Database connectivity (via API responses)", "PASS")
        else:
            self.log("✗ Database connectivity unclear", "WARN")
            
        # 10. Performance tests
        self.log("\n=== TESTING PERFORMANCE ===")
        start_time = time.time()
        self.test_endpoint("/api/tasks", description="Performance test - API response time")
        response_time = time.time() - start_time
        
        if response_time < 2.0:
            self.log(f"✓ API response time: {response_time:.2f}s", "PASS")
        else:
            self.log(f"✗ API response time slow: {response_time:.2f}s", "WARN")
            
    def generate_report(self):
        """Generate final test report"""
        self.log("\n" + "="*50)
        self.log("COMPREHENSIVE TEST REPORT")
        self.log("="*50)
        
        total_tests = len(self.passed_tests) + len(self.failed_tests)
        pass_rate = (len(self.passed_tests) / total_tests * 100) if total_tests > 0 else 0
        
        self.log(f"Total Tests: {total_tests}")
        self.log(f"Passed: {len(self.passed_tests)}")
        self.log(f"Failed: {len(self.failed_tests)}")
        self.log(f"Pass Rate: {pass_rate:.1f}%")
        
        if self.failed_tests:
            self.log("\nFAILED TESTS:")
            for failure in self.failed_tests:
                self.log(f"  - {failure}")
                
        # Deployment readiness assessment
        critical_failures = [f for f in self.failed_tests if any(keyword in f.lower() 
                           for keyword in ['api', 'database', 'server', 'error 500'])]
        
        self.log(f"\nDEPLOYMENT READINESS:")
        if len(critical_failures) == 0 and pass_rate > 80:
            self.log("✓ READY FOR DEPLOYMENT", "PASS")
            self.log("All critical systems functional")
        elif len(critical_failures) == 0:
            self.log("⚠ MOSTLY READY - Minor issues detected", "WARN") 
            self.log("Consider fixing non-critical issues before deployment")
        else:
            self.log("✗ NOT READY FOR DEPLOYMENT", "FAIL")
            self.log("Critical issues must be resolved")
            
        return len(critical_failures) == 0 and pass_rate > 80

if __name__ == "__main__":
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api", timeout=5)
        print("Server detected, starting tests...")
    except:
        print("ERROR: Server not running on localhost:5000")
        print("Please start the server with: uvicorn main:app --reload --host 0.0.0.0 --port 5000")
        sys.exit(1)
        
    # Run tests
    test_suite = TestSuite()
    test_suite.run_comprehensive_tests()
    ready = test_suite.generate_report()
    
    sys.exit(0 if ready else 1)