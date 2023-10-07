"""This is test only for local dev machine"""

import unittest
from client import get_page


class ScrapperTest(unittest.TestCase):
    api_key = "-dtN4sIxhcJYSqMV5P7Jj9EFn1F1lGkfbrt"
    base_api_url = "http://localhost:9000/api/get?url="

    def test_auth(self):
        result = get_page(
            url="https://ya.ru/", base_api_url=self.base_api_url, api_key="123"
        )
        self.assertEqual(result["error"], "Api key is invalid")

    def test_404(self):
        result = get_page(
            url="https://linux.org.ru/404",
            base_api_url=self.base_api_url,
            api_key=self.api_key,
        )
        self.assertEqual(int(result["status_code"]), 404)

    def test_selenium(self):
        result = get_page(
            url="https://scrapper.scurra.space/",
            base_api_url=self.base_api_url,
            api_key=self.api_key,
            referer="https://google.com/",
            use_selenium=True,
        )
        self.assertEqual(result["selenium"], True)
        self.assertIn("website scraping", result["html"])
        self.assertEqual(int(result["status_code"]), 200)


if __name__ == "__main__":
    unittest.main()
