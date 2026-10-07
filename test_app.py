import unittest

from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertEqual(
            response.get_json(),
            {
                "name": "deliveryai-demo-app",
                "message": "Welcome to DeliveryAI Demo",
            },
        )


if __name__ == "__main__":
    unittest.main()
