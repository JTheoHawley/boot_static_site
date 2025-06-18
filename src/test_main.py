import unittest
from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        md = """# Heading One  

Paragraph one

### **BOLD** Heading Three"""
        expected = "Heading One"
        converted = extract_title(md)
        self.assertEqual(expected, converted)



if __name__ == "__main__":
    unittest.main()