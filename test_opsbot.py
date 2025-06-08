#!/usr/bin/env python3
"""
Simple test script for OpsBot functionality
"""
import json
import pandas as pd
import sys
import os

def test_data_loading():
    """Test that systems.json loads correctly"""
    try:
        with open('systems.json', 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        
        # Basic validation
        assert len(data) > 0, "No systems loaded"
        assert all(key in data[0] for key in ['name', 'status', 'cpu', 'memory']), "Missing required fields"
        
        print(f"✅ Data loading test passed - {len(data)} systems loaded")
        return True
    except Exception as e:
        print(f"❌ Data loading test failed: {e}")
        return False

def test_data_filtering():
    """Test data filtering functionality"""
    try:
        with open('systems.json', 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        
        # Test filtering stopped systems
        stopped_systems = df[df['status'] == 'stopped']
        print(f"✅ Found {len(stopped_systems)} stopped systems")
        
        # Test filtering high memory systems
        high_memory = df[df['memory'] > 80]
        print(f"✅ Found {len(high_memory)} systems with memory > 80%")
        
        # Test filtering high CPU systems  
        high_cpu = df[df['cpu'] > 80]
        print(f"✅ Found {len(high_cpu)} systems with CPU > 80%")
        
        return True
    except Exception as e:
        print(f"❌ Data filtering test failed: {e}")
        return False

def test_app_imports():
    """Test that the app can be imported without errors"""
    try:
        # Add current directory to path for imports
        sys.path.insert(0, os.getcwd())
        
        # Test importing key functions from app
        import app
        
        # Test loading system data function
        df = app.load_system_data()
        assert not df.empty, "System data should not be empty"
        
        print("✅ App import test passed")
        return True
    except Exception as e:
        print(f"❌ App import test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running OpsBot tests...")
    
    tests = [
        test_data_loading,
        test_data_filtering,
        test_app_imports
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1

if __name__ == "__main__":
    exit(main())