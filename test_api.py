#!/usr/bin/env python3
"""
Test script for EV Charging Station Predictor API
This script tests all the API endpoints to ensure they're working correctly.
"""

import requests
import json
import time
import sys
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_endpoint(endpoint: str, method: str = "GET", data: Dict[Any, Any] = None) -> bool:
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=TIMEOUT)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=TIMEOUT)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        if response.status_code == 200:
            print(f"✅ {method} {endpoint} - Success")
            return True
        else:
            print(f"❌ {method} {endpoint} - Failed (Status: {response.status_code})")
            print(f"   Response: {response.text[:100]}...")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {method} {endpoint} - Error: {e}")
        return False

def wait_for_server(max_attempts: int = 30) -> bool:
    """Wait for the server to become available"""
    print(f"🔍 Waiting for server at {BASE_URL}...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/api/stats", timeout=5)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"   Attempt {attempt + 1}/{max_attempts} - waiting...")
        time.sleep(2)
    
    print(f"❌ Server not available after {max_attempts} attempts")
    return False

def run_api_tests() -> bool:
    """Run all API tests"""
    print("🧪 Starting API Tests")
    print("=" * 50)
    
    # Test data for prediction
    test_location = {
        "locations": [{
            "latitude": 28.6139,
            "longitude": 77.209,
            "parking": 5,
            "restaurant": 3,
            "school": 2,
            "commercial": 8,
            "population": 7500,
            "park": 1,
            "edges": 10,
            "parking_space": 20,
            "civic": 1,
            "node": 15,
            "community_centre": 1,
            "place_of_worship": 2,
            "university": 0,
            "cinema": 1,
            "library": 1,
            "retail": 5,
            "townhall": 0,
            "government": 1,
            "residential": 50
        }],
        "model_name": "xgboost"
    }
    
    # List of tests to run
    tests = [
        # GET endpoints
        ("GET", "/", None),
        ("GET", "/api/stats", None),
        ("GET", "/api/models", None),
        ("GET", "/api/existing-predictions?limit=10", None),
        ("GET", "/api/feature-importance", None),
        ("GET", "/api/map", None),
        
        # POST endpoints
        ("POST", "/api/predict", test_location),
    ]
    
    passed = 0
    failed = 0
    
    for method, endpoint, data in tests:
        if test_endpoint(endpoint, method, data):
            passed += 1
        else:
            failed += 1
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed.")
        return False

def test_prediction_models() -> bool:
    """Test prediction with different models"""
    print("\n🤖 Testing ML Models")
    print("-" * 30)
    
    models = ["xgboost", "catboost", "gradient_boosting"]
    test_location = {
        "locations": [{
            "latitude": 28.6139,
            "longitude": 77.209,
            "parking": 5,
            "restaurant": 3,
            "school": 2,
            "commercial": 8,
            "population": 7500,
            "park": 1,
            "edges": 0,
            "parking_space": 0,
            "civic": 0,
            "node": 0,
            "community_centre": 0,
            "place_of_worship": 0,
            "university": 0,
            "cinema": 0,
            "library": 0,
            "retail": 0,
            "townhall": 0,
            "government": 0,
            "residential": 0
        }]
    }
    
    for model in models:
        test_location["model_name"] = model
        print(f"🔬 Testing {model} model...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/predict",
                json=test_location,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                prediction = result["predictions"][0]
                print(f"   ✅ {model}: {prediction['recommendation']} "
                      f"(Confidence: {prediction['confidence']:.1%})")
            else:
                print(f"   ❌ {model}: Failed (Status: {response.status_code})")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {model}: Error - {e}")
    
    return True

def main():
    """Main test function"""
    print("🔋 EV Charging Station Predictor - API Test Suite")
    print("=" * 60)
    
    # Check if server is available
    if not wait_for_server():
        print("\n❌ Cannot connect to server. Please ensure the application is running.")
        print("💡 Start the server with: python app.py")
        sys.exit(1)
    
    # Run basic API tests
    api_success = run_api_tests()
    
    # Test ML models
    model_success = test_prediction_models()
    
    # Final results
    print("\n" + "=" * 60)
    if api_success and model_success:
        print("🎉 All tests completed successfully!")
        print("✅ Your EV Station Predictor is ready for use!")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()