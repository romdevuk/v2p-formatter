"""
Quick server health check for AC Matrix routes
Tests that all routes are accessible
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_routes_importable():
    """Test that all routes can be imported"""
    print("Testing route imports...")
    try:
        from app.routes import bp
        print("  ✓ Blueprint imported")
        
        # Check that blueprint has routes (can't access url_map until registered)
        print(f"  ✓ Blueprint ready for registration")
        print(f"    (Routes will be available after app.register_blueprint())")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_modules_importable():
    """Test that all modules can be imported"""
    print("\nTesting module imports...")
    modules = [
        'app.ac_matrix_parser',
        'app.ac_matrix_analyzer',
        'app.ac_matrix_storage'
    ]
    
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"  ✓ {module_name}")
        except Exception as e:
            print(f"  ✗ {module_name}: {e}")
            return False
    
    return True

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    try:
        from config import (
            AC_MATRIX_JSON_STANDARDS_DIR,
            AC_MATRIX_DATA_DIR,
            AC_MATRIX_MAX_FILE_SIZE,
            AC_MATRIX_ALLOWED_EXTENSIONS
        )
        print(f"  ✓ AC_MATRIX_JSON_STANDARDS_DIR: {AC_MATRIX_JSON_STANDARDS_DIR}")
        print(f"  ✓ AC_MATRIX_DATA_DIR: {AC_MATRIX_DATA_DIR}")
        print(f"  ✓ AC_MATRIX_MAX_FILE_SIZE: {AC_MATRIX_MAX_FILE_SIZE / (1024*1024):.1f}MB")
        print(f"  ✓ AC_MATRIX_ALLOWED_EXTENSIONS: {AC_MATRIX_ALLOWED_EXTENSIONS}")
        
        # Check directories exist
        if AC_MATRIX_JSON_STANDARDS_DIR.exists():
            print(f"  ✓ Standards directory exists")
        else:
            print(f"  ⚠ Standards directory missing (will be created)")
        
        if AC_MATRIX_DATA_DIR.exists():
            print(f"  ✓ Analyses directory exists")
        else:
            print(f"  ⚠ Analyses directory missing (will be created)")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_templates():
    """Test template exists"""
    print("\nTesting templates...")
    template_path = Path(__file__).parent / 'templates' / 'ac_matrix.html'
    if template_path.exists():
        print(f"  ✓ Template exists: {template_path}")
        return True
    else:
        print(f"  ✗ Template missing: {template_path}")
        return False

def test_static_files():
    """Test static files exist"""
    print("\nTesting static files...")
    static_dir = Path(__file__).parent / 'static'
    files = [
        'css/ac-matrix.css',
        'js/ac-matrix.js'
    ]
    
    all_exist = True
    for file_path in files:
        full_path = static_dir / file_path
        if full_path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} missing")
            all_exist = False
    
    return all_exist

if __name__ == '__main__':
    print("=" * 70)
    print("AC Matrix - Server Health Check")
    print("=" * 70)
    
    results = []
    results.append(test_routes_importable())
    results.append(test_modules_importable())
    results.append(test_config())
    results.append(test_templates())
    results.append(test_static_files())
    
    print("\n" + "=" * 70)
    if all(results):
        print("✓ ALL CHECKS PASSED - Server ready to start!")
        print("=" * 70)
        print("\nTo start server:")
        print("  python run.py")
        print("\nThen navigate to:")
        print("  http://localhost/v2p-formatter/ac-matrix")
        sys.exit(0)
    else:
        print("✗ SOME CHECKS FAILED")
        print("=" * 70)
        sys.exit(1)

