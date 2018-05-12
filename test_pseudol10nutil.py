# -*- coding: utf-8 -*-

import unittest

from pseudol10nutil import PseudoL10nUtil
import pseudol10nutil.transforms


class TestPseudoL10nUtil(unittest.TestCase):

    def setUp(self):
        self.util = PseudoL10nUtil()
        self.test_data = u"The quick brown fox jumps over the lazy dog"

    def test_default(self):
        expected = u"⟦Ťȟê ʠüıċǩ ƀȓøẁñ ƒøẋ ǰüɱƥš øṽêȓ ťȟê ĺàźÿ đøğ﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘🚦﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘🚦﹎Ѝ⟧"
        self.assertEqual(expected, self.util.pseudolocalize(self.test_data))

    def test_transliterate_diacritic(self):
        expected = u"Ťȟê ʠüıċǩ ƀȓøẁñ ƒøẋ ǰüɱƥš øṽêȓ ťȟê ĺàźÿ đøğ"
        self.util.transforms = [pseudol10nutil.transforms.transliterate_diacritic]
        self.assertEqual(expected, self.util.pseudolocalize(self.test_data))

    def test_transliterate_circled(self):
        expected = u"Ⓣⓗⓔ ⓠⓤⓘⓒⓚ ⓑⓡⓞⓦⓝ ⓕⓞⓧ ⓙⓤⓜⓟⓢ ⓞⓥⓔⓡ ⓣⓗⓔ ⓛⓐⓩⓨ ⓓⓞⓖ"
        self.util.transforms = [pseudol10nutil.transforms.transliterate_circled]
        self.assertEqual(expected, self.util.pseudolocalize(self.test_data))

    def test_transliterate_fullwidth(self):
        expected = u"Ｔｈｅ ｑｕｉｃｋ ｂｒｏｗｎ ｆｏｘ ｊｕｍｐｓ ｏｖｅｒ ｔｈｅ ｌａｚｙ ｄｏｇ"
        self.util.transforms = [pseudol10nutil.transforms.transliterate_fullwidth]
        self.assertEqual(expected, self.util.pseudolocalize(self.test_data))

    def test_angle_brackets(self):
        expected = u"《The quick brown fox jumps over the lazy dog》"
        self.util.transforms = [pseudol10nutil.transforms.angle_brackets]
        self.assertEqual(expected, self.util.pseudolocalize(self.test_data))

    def test_curly_brackets(self):
        expected = u"❴The quick brown fox jumps over the lazy dog❵"
        self.util.transforms = [pseudol10nutil.transforms.curly_brackets]
        self.assertEqual(expected, self.util.pseudolocalize(self.test_data))

    def test_square_brackets(self):
        expected = u"⟦The quick brown fox jumps over the lazy dog⟧"
        self.util.transforms = [pseudol10nutil.transforms.square_brackets]
        self.assertEqual(expected, self.util.pseudolocalize(self.test_data))

    def test_pad_length(self):
        expected = u"The quick brown fox jumps over the lazy dog﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘🚦﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘🚦﹎Ѝ"
        self.util.transforms = [pseudol10nutil.transforms.pad_length]
        self.assertEqual(expected, self.util.pseudolocalize(self.test_data))


if __name__ == "__main__":
    unittest.main()
