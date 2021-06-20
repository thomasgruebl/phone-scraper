import unittest

from phonescraper import helpers
from phonescraper import scraper


class BasicTest(unittest.TestCase):

    @unittest.skipIf(helpers.Args().parse_args() == 1, "email argument not given")
    def test_email(self):
        self.assertIn(helpers.Email.receiver, "@")

    def test_sites_json(self):
        self.assertIsNotNone(scraper.initialise())

    def test_phone_session_call(self):
        self.assertIsNotNone(scraper.get_free_phone_list(session=None))

    def test_message_session_call(self):
        self.assertIsNotNone(scraper.get_free_message_list(session=None, phone_number="+46700000000"))


if __name__ == '__main__':
    unittest.main()
