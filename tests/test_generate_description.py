# TODO: not finished
import unittest
from src.main import generate_description

class TestCallLLMFunction(unittest.TestCase):
    def test_call_generate_description(self):
        # Call the function
        category = "Ancient Rome"
        keywords = ["Caesar", "Legion", "Coliseum", "Rome baths"]
        result = generate_description(category, keywords)

        # Validate the result
        self.assertIn(
            result,
            keywords
        )

if __name__ == '__main__':
    unittest.main()