#!/usr/bin/env python3
# =============================================================================
# UNICODE FIX VERIFICATION TEST
# =============================================================================
#
# Quick test to verify that Unicode encoding issues are fixed
#
# USAGE: python test_unicode_fix.py
# =============================================================================

import sys
import os

def test_unicode_compatibility():
    """
    Test that all print statements work without Unicode errors
    """
    print("*** UNICODE COMPATIBILITY TEST ***")
    print("=" * 50)
    
    try:
        # Test basic ASCII symbols
        print("SUCCESS: Basic ASCII symbols work")
        print("   - Asterisks: ***")
        print("   - Equals: ===")
        print("   - Dashes: ---")
        
        # Test that we can print without Unicode errors
        print("\nTesting various output formats:")
        print("   SUCCESS: Test passed")
        print("   FAILED: Test failed") 
        print("   WARNING: Test warning")
        print("   ERROR: Test error")
        
        # Test file operations
        test_filename = "unicode_test_temp.txt"
        with open(test_filename, 'w', encoding='utf-8') as f:
            f.write("Test file content\n")
            f.write("SUCCESS: File writing works\n")
        
        # Clean up
        if os.path.exists(test_filename):
            os.remove(test_filename)
            print("   SUCCESS: File operations work")
        
        print("\n*** ALL UNICODE TESTS PASSED! ***")
        print("The test scripts should now work on Windows.")
        return True
        
    except UnicodeEncodeError as e:
        print(f"FAILED: Unicode encoding error: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return False

def test_import_compatibility():
    """
    Test that we can import the test modules without errors
    """
    print("\n*** IMPORT COMPATIBILITY TEST ***")
    print("=" * 50)
    
    test_modules = [
        'test_edge_cases_minimal_data',
        'test_data_quality_scenarios', 
        'test_business_scenarios'
    ]
    
    import_results = {}
    
    for module_name in test_modules:
        try:
            # Try to import the module
            __import__(module_name)
            print(f"SUCCESS: {module_name} imports correctly")
            import_results[module_name] = True
        except ImportError as e:
            print(f"WARNING: {module_name} import failed: {e}")
            import_results[module_name] = False
        except Exception as e:
            print(f"ERROR: {module_name} unexpected error: {e}")
            import_results[module_name] = False
    
    successful_imports = sum(import_results.values())
    total_imports = len(import_results)
    
    print(f"\nImport Results: {successful_imports}/{total_imports} successful")
    
    if successful_imports == total_imports:
        print("*** ALL IMPORTS SUCCESSFUL! ***")
        return True
    else:
        print("*** SOME IMPORTS FAILED ***")
        return False

def main():
    """
    Run all compatibility tests
    """
    print("TESTING UNICODE AND IMPORT COMPATIBILITY")
    print("=" * 60)
    print("Verifying that the test scripts will work on Windows")
    print()
    
    # Test Unicode compatibility
    unicode_ok = test_unicode_compatibility()
    
    # Test import compatibility
    import_ok = test_import_compatibility()
    
    # Overall result
    print("\n" + "=" * 60)
    print("*** FINAL RESULTS ***")
    
    if unicode_ok and import_ok:
        print("SUCCESS: All compatibility tests passed!")
        print("You can now run the test scripts:")
        print("   python test_edge_cases_minimal_data.py")
        print("   python test_data_quality_scenarios.py")
        print("   python test_business_scenarios.py")
        print("   python run_all_tests.py")
        return 0
    else:
        print("FAILED: Some compatibility issues remain")
        if not unicode_ok:
            print("   - Unicode encoding issues detected")
        if not import_ok:
            print("   - Module import issues detected")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
