#!/usr/bin/env python3
# Quick script to fix all Unicode characters in test files

import re
import os

def fix_unicode_in_file(filename):
    """Fix Unicode characters in a file"""
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return
    
    # Unicode replacements
    replacements = {
        '✅': 'SUCCESS:',
        '❌': 'FAILED:',
        '⚠️': 'WARNING:',
        '📊': '',
        '💰': '',
        '📈': '',
        '📏': '',
        '💾': '',
        '🔍': '',
        '💼': '',
        '📋': '',
        '🚀': '',
        '🎯': '',
        '🧪': '',
        '📄': '',
        '💡': '',
        '🎉': '',
        '📁': '',
        '⏰': 'TIMEOUT:',
        '🔧': '',
        '🎯': '',
        '📋': ''
    }
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply replacements
        for unicode_char, replacement in replacements.items():
            content = content.replace(unicode_char, replacement)
        
        # Clean up extra spaces
        content = re.sub(r'   +', '   ', content)  # Multiple spaces to 3 spaces
        content = re.sub(r'f"  +', 'f"   ', content)  # Clean f-string formatting
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed Unicode in: {filename}")
        
    except Exception as e:
        print(f"Error fixing {filename}: {e}")

def main():
    """Fix Unicode in all test files"""
    test_files = [
        'test_edge_cases_minimal_data.py',
        'test_data_quality_scenarios.py',
        'test_business_scenarios.py',
        'run_all_tests.py'
    ]
    
    print("Fixing Unicode characters in test files...")
    
    for filename in test_files:
        fix_unicode_in_file(filename)
    
    print("Unicode fix complete!")

if __name__ == "__main__":
    main()
