import unittest

import requests

from pseudol10nutil import PseudoL10nUtil


base_url = "http://localhost:5000/pseudol10nutil/api/v1.0/"
headers = {"Accept": "application/json", "Content-Type": "application/json"}


class TestPseudoL10nUtil(unittest.TestCase):

    def setUp(self):
        self.util = PseudoL10nUtil()

    def test_pseudo(self):
        data = {
            "key1": u"The quick brown fox jumps over the lazy dog.",
            "key2": u"The quick brown {animal1} jumps over the lazy {animal2}.",
            "key3": u"The quick brown %s jumps over the lazy %s.",
            "key4": u"The quick brown %(animal1)s jumps over the lazy %(animal2)s."
        }
        request_data = {
            "strings": data
        }
        resp = requests.post(base_url + "pseudo", json=request_data)
        results = resp.json()["strings"]
        for k, v in results.items():
            self.assertEqual(self.util.pseudolocalize(data[k]), v)


if __name__ == "__main__":
    unittest.main()
