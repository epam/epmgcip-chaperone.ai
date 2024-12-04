# TODO: not finished
import unittest
from src.main import generate_description
from src.main import translate_text

class TestCallLLMFunction(unittest.TestCase):
    def test_call_generate_description(self):
        # Call the function
        category = "Ancient Rome"
        keywords = ["Caesar", "Legion", "Coliseum", "Rome baths"]
        result = generate_description(category, keywords).lower()
        print(result)

        # Validate the result
        for keyword in keywords:
            print("Checking: " + keyword + "..")
            # not 100% reliable yet, since the expected words might be slighly changed
            self.assertIn(
                keyword.lower(),
                result
            )

    def test_call_translate_text(self):
            # Call the function
            text = ("PROLOGUE: "
        "Two households, both alike in dignity,"
        "In fair Verona, where we lay our scene,"
        "From ancient grudge break to new mutiny,"
        "Where civil blood makes civil hands unclean."
        "From forth the fatal loins of these two foes"
        "A pair of star-cross'd lovers take their life;"
        "Whose misadventured piteous overthrows"
        "Do with their death bury their parents' strife."
        "The fearful passage of their death-mark'd love,"
        "And the continuance of their parents' rage,"
        "Which, but their children's end, nought could remove,"
        "Is now the two hours' traffic of our stage;"
        "The which if you with patient ears attend,"
        "What here shall miss, our toil shall strive to mend.")
            translated_text = translate_text(text=text, language="Belarussian").lower()
            print(translated_text)

            # Validate the result
            # for keyword in keywords:
            #     print("Checking: " + keyword + "..")
            #     # not 100% reliable yet, since the expected words might be slighly changed
            #     self.assertIn(
            #         keyword.lower(),
            #         result
            #     )            

if __name__ == '__main__':
    unittest.main(exit=False)