import unittest

from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    # REQ-002: 首页零回归
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

    # REQ-001.1 / 001.2 / 001.3: 健康检查 200 + JSON + 精确响应体
    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertIn("application/json", response.content_type)
        self.assertEqual(response.get_json(), {"status": "ok"})

    # REQ-001.7: 幂等与无副作用 —— 连续两次调用结果完全一致
    def test_health_idempotent(self):
        r1 = self.client.get("/health")
        r2 = self.client.get("/health")
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r1.get_json(), {"status": "ok"})
        self.assertEqual(r2.get_json(), {"status": "ok"})
        self.assertEqual(r1.get_json(), r2.get_json())

    # REQ-001.8: 非 GET 方法沿用 Flask 默认 405 Method Not Allowed
    def test_health_method_not_allowed(self):
        for method in ("post", "put", "delete", "patch"):
            with self.subTest(method=method):
                response = getattr(self.client, method)("/health")
                self.assertEqual(
                    response.status_code, 405,
                    msg=f"{method.upper()} /health 应返回 405",
                )


if __name__ == "__main__":
    unittest.main()
