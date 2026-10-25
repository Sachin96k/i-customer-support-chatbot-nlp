"""Small tests for chatbot response handling. Run with: python -m unittest discover -s tests"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import app as chatbot_app

class ChatbotTests(unittest.TestCase):
    def setUp(self):
        self.client = chatbot_app.app.test_client()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Customer Support", response.data)

    def test_empty_message_is_handled(self):
        result = chatbot_app.get_reply("   ")
        self.assertIn("reply", result)
        self.assertEqual(result["intent"], "empty")

    def test_chat_endpoint_rejects_non_text(self):
        response = self.client.post("/chat", json={"message": 123})
        self.assertEqual(response.status_code, 400)

    def test_chat_endpoint_rejects_long_message(self):
        response = self.client.post("/chat", json={"message": "a" * 1001})
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
