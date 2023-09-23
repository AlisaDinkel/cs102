import unittest
import octobot
from datetime import datetime


class TestOctobot(unittest.TestCase):
    def test_is_valid_date(self):
        self.assertFalse(octobot.is_valid_date("29/02/23", "/"))
        self.assertFalse(octobot.is_valid_date("30/02/24", "/"))
        self.assertTrue(octobot.is_valid_date("29/02/24", "/"))
        self.assertFalse(octobot.is_valid_date("01/01/23", "/"))
        self.assertFalse(octobot.is_valid_date("04/05/23", "."))
        self.assertFalse(octobot.is_valid_date("09/04.23", "."))
        self.assertTrue(octobot.is_valid_date("05/05/23", "/"))
        today = datetime.today().date().strftime("%d/%m/%y")
        self.assertTrue(octobot.is_valid_date(today, "/"))
        self.assertFalse(octobot.is_valid_date("05/09/30", "/"))
        self.assertTrue(octobot.is_valid_date("04.05.23", "."))
        self.assertFalse(octobot.is_valid_date("35/04/23", "/"))

    def test_is_valid_url(self):
        self.assertTrue(octobot.is_valid_url("https://itmo.ru"))
        self.assertTrue(octobot.is_valid_url("itmo.ru"))
        self.assertTrue(octobot.is_valid_url("www.itmo.ru"))
        self.assertTrue(octobot.is_valid_url("http://itmo.ru"))
        self.assertFalse(octobot.is_valid_url("https://itmo."))
        self.assertFalse(octobot.is_valid_url("https://itmo"))
        self.assertFalse(octobot.is_valid_url("itmo"))
        self.assertFalse(octobot.is_valid_url("itmo."))
        self.assertTrue(octobot.is_valid_url("https://en.itmo.ru"))
        self.assertFalse(octobot.is_valid_url("en.itmo.ru"))
        self.assertFalse(octobot.is_valid_url("en.itmo"))


if __name__ == "__main__":
    unittest.main()
