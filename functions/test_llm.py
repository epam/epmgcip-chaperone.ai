import json
from unittest import TestCase

from azure.functions import HttpRequest

from functions.function_app import translate_http_trigger

class FunctionUnitTests(TestCase):
    def test_translate_text(self):
        # send an empty body, the function only requires parameters from the query string
        request = HttpRequest(
            method="POST",
            url="http://localhost:7071/api/translate_http_trigger",
            body="",
            params={"text": "Hello World!", "language": "Belarussian" },
        )
        # call the Azure Function
        response = translate_http_trigger(request)
        # load the response body as JSON
        j = json.loads(response.get_body())

        # the function was executed without errors
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.mimetype)

        for keyword in ["Прывітанне", "Свет"]:
            print("\nChecking: " + keyword + "..")
            # not 100% reliable yet, since the expected words might be slighly changed
            self.assertIn(
                keyword.lower(),
                j["LLM Response"].lower()
            )
