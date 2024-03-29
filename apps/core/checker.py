import json

from django.test import TestCase


class BaseChecker(TestCase):
    # Ok
    def assertResponse200(self, response):
        self.assertEqual(response.status_code, 200)

    # Created
    def assertResponse201(self, response):
        self.assertEqual(response.status_code, 201)

    # Bad request
    def assertResponse400(self, response):
        self.assertEqual(response.status_code, 400)

    # Unauthorized
    def assertResponse401(self, response):
        self.assertEqual(response.status_code, 401)

    # Not found
    def assertResponse404(self, response):
        self.assertEqual(response.status_code, 404)

    def loadJSONSafely(self, response):
        try:
            return json.loads(response.content)
        except ValueError:
            self.fail("Couldn't load the JSON data safely.")
