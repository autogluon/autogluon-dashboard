import unittest
from aggregate_file import get_imports, extract_code


class TestAggregate(unittest.TestCase):
    def test_get_code(self):
        code = extract_code("tests/unittests/mock_python_file/mock_file.py")
        expected_code = """# This file is only consumed by test_aggregate.py to test the aggregation functions from the aggregate_file.py script.


def code():
    a = 1
    b = 2
    return lambda x: x + a*b"""
        self.assertEqual(code, expected_code)
    
    def test_get_imports(self):
        imports = get_imports("tests/unittests/mock_python_file/mock_file.py")
        imports = sorted(list(imports))
        self.assertEqual(imports[0], "from module import pkg")
        self.assertEqual(imports[1], "from module import pkg as name")
        self.assertEqual(imports[2], "from module.sub_module import pkg as name")
        self.assertEqual(imports[3], "import pandas")
        self.assertEqual(imports[4], "import pandas as pd")
        self.assertEqual(imports[5], "import panel")
        self.assertEqual(imports[6], "import pkg.sub_pkg")
        self.assertEqual(imports[7], "import pkg.sub_pkg as name")
        
if __name__ == "__main__":
    unittest.main()
