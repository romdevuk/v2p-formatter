"""Test AC Matrix Storage"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.ac_matrix_storage import save_matrix, list_matrices, load_matrix, delete_matrix

test_data = {
    'total_ac_count': 10,
    'covered_ac_count': 5,
    'missing_ac_count': 5,
    'coverage_percentage': 50.0,
    'units': []
}

print("Testing Storage Operations...")
result = save_matrix(test_data, 'Test Matrix', 'test-file', 'test.json', 'Test observation')
print(f"Save: {result['success']}")

matrices = list_matrices()
print(f"List: {len(matrices)} matrices")

if matrices:
    matrix_id = matrices[0]['matrix_id']
    loaded = load_matrix(matrix_id)
    print(f"Load: {loaded['success']}")
    
    delete_result = delete_matrix(matrix_id)
    print(f"Delete: {delete_result['success']}")
    
    matrices_after = list_matrices()
    print(f"List after delete: {len(matrices_after)} matrices")

print("Storage tests complete!")




