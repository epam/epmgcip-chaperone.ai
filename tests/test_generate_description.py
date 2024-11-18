# TODO: not finished
import unittest
from src.main import generate_description

class TestCallLLMFunction(unittest.TestCase):
    def test_call_generate_description(self):
        # Call the function
        category = "Ancient Rome"
        keywords = ["Caesar", "Legion", "Coliseum", "Rome baths"]
        result = generate_description(category, keywords).lower()

        # Validate the result
        for keyword in keywords:
            print("Checking: " + keyword + "..")
            # not 100% reliable yet, since the expected words might be slighly changed
            self.assertIn(
                keyword.lower(),
                result
            )

if __name__ == '__main__':
    unittest.main(exit=False)