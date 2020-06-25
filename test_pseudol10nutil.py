# -*- coding: utf-8 -*-

import filecmp
import os.path
import unittest

from pseudol10nutil import POFileUtil, PseudoL10nUtil
import pseudol10nutil.transforms


class TestPOFileUtil(unittest.TestCase):

    def setUp(self):
        self.pofileutil = POFileUtil()

    def test_generate_pseudolocalized_po(self):
        input_file = "./testdata/locales/helloworld.pot"
        expected_file = "./testdata/locales/eo/LC_MESSAGES/helloworld.po"
        basename, ext = os.path.splitext(expected_file)
        generated_file = basename + "_generated" + ext
        self.pofileutil.pseudolocalizefile(input_file, generated_file)
        self.assertTrue(filecmp.cmp(expected_file, generated_file))
        os.remove(generated_file)


class TestPseudoL10nUtil(unittest.TestCase):

    def setUp(self):
        self.util = PseudoL10nUtil()
        self.test_data = u"The quick brown fox jumps over the lazy dog"

    def test_default(self):
        expected = u"⟦Ťȟê ʠüıċǩ ƀȓøẁñ ƒøẋ ǰüɱƥš øṽêȓ ťȟê ĺàźÿ đøğ﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘🚦﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘🚦﹎Ѝ⟧"
        self.assertEqual(expected, self.util.pseudolocalize(self.test_data))

    def test_empty_string(self):
        self.assertEqual(u"", self.util.pseudolocalize(u""))
        self.assertEqual(u"", self.util.pseudolocalize(None))

    def test_default_fmtspec(self):
        test_data_fmtspec = u"The quick brown {0} jumps over the lazy {1}."
        expected = u"⟦Ťȟê ʠüıċǩ ƀȓøẁñ {0} ǰüɱƥš øṽêȓ ťȟê ĺàźÿ {1}.﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘🚦﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘🚦﹎Ѝא⟧"
        self.assertEqual(expected, self.util.pseudolocalize(test_data_fmtspec))
        test_data_fmtspec = u"The quick brown {animal1} jumps over the lazy {animal2}."
        expected = u"⟦Ťȟê ʠüıċǩ ƀȓøẁñ {animal1} ǰüɱƥš øṽêȓ ťȟê ĺàźÿ {animal2}.﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘🚦﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘⟧"
        self.assertEqual(expected, self.util.pseudolocalize(test_data_fmtspec))

    def test_default_printffmtspec(self):
        test_data_printffmtspec = u"The quick brown %s jumps over the lazy %s."
        expected = u"⟦Ťȟê ʠüıċǩ ƀȓøẁñ %s ǰüɱƥš øṽêȓ ťȟê ĺàźÿ %s.﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘🚦﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘🚦﹎Ѝ⟧"
        self.assertEqual(expected, self.util.pseudolocalize(test_data_printffmtspec))
        test_data_printffmtspec = u"The quick brown %(animal1)s jumps over the lazy %(animal2)s."
        expected = u"⟦Ťȟê ʠüıċǩ ƀȓøẁñ %(animal1)s ǰüɱƥš øṽêȓ ťȟê ĺàźÿ %(animal2)s.﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘🚦﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘🚦⟧"
        self.assertEqual(expected, self.util.pseudolocalize(test_data_printffmtspec))

    def test_transliterate_diacritic(self):
        expected = u"Ťȟê ʠüıċǩ ƀȓøẁñ ƒøẋ ǰüɱƥš øṽêȓ ťȟê ĺàźÿ đøğ"
        self.util.transforms = [pseudol10nutil.transforms.transliterate_diacritic]
        self.assertEqual(expected, self.util.pseudolocalize(self.test_data))
        test_data_fmtspec = u"Source {0} returned 0 rows, source {1} returned 1 row."
        expected = u"Șøüȓċê {0} ȓêťüȓñêđ 0 ȓøẁš, šøüȓċê {1} ȓêťüȓñêđ 1 ȓøẁ."
        self.assertEqual(expected, self.util.pseudolocalize(test_data_fmtspec))
        test_data_printffmtspec = u"Source %(source0)s returned 0 rows, source %(source1)s returned 1 row."
        expected = u"Șøüȓċê %(source0)s ȓêťüȓñêđ 0 ȓøẁš, šøüȓċê %(source1)s ȓêťüȓñêđ 1 ȓøẁ."
        self.assertEqual(expected, self.util.pseudolocalize(test_data_printffmtspec))
        test_data_printffmtspec = u"Source %s returned %d rows."
        expected = u"Șøüȓċê %s ȓêťüȓñêđ %d ȓøẁš."
        self.assertEqual(expected, self.util.pseudolocalize(test_data_printffmtspec))

    def test_transliterate_circled(self):
        expected = u"Ⓣⓗⓔ ⓠⓤⓘⓒⓚ ⓑⓡⓞⓦⓝ ⓕⓞⓧ ⓙⓤⓜⓟⓢ ⓞⓥⓔⓡ ⓣⓗⓔ ⓛⓐⓩⓨ ⓓⓞⓖ"
        self.util.transforms = [pseudol10nutil.transforms.transliterate_circled]
        self.assertEqual(expected, self.util.pseudolocalize(self.test_data))
        test_data_fmtspec = u"Source {0} returned 0 rows, source {1} returned 1 row."
        expected = u"Ⓢⓞⓤⓡⓒⓔ {0} ⓡⓔⓣⓤⓡⓝⓔⓓ ⓪ ⓡⓞⓦⓢ, ⓢⓞⓤⓡⓒⓔ {1} ⓡⓔⓣⓤⓡⓝⓔⓓ ① ⓡⓞⓦ."
        self.assertEqual(expected, self.util.pseudolocalize(test_data_fmtspec))
        test_data_printffmtspec = u"Source %(source0)s returned 0 rows, source %(source1)s returned 1 row."
        expected = u"Ⓢⓞⓤⓡⓒⓔ %(source0)s ⓡⓔⓣⓤⓡⓝⓔⓓ ⓪ ⓡⓞⓦⓢ, ⓢⓞⓤⓡⓒⓔ %(source1)s ⓡⓔⓣⓤⓡⓝⓔⓓ ① ⓡⓞⓦ."
        self.assertEqual(expected, self.util.pseudolocalize(test_data_printffmtspec))
        test_data_printffmtspec = u"Source %s returned %d rows."
        expected = u"Ⓢⓞⓤⓡⓒⓔ %s ⓡⓔⓣⓤⓡⓝⓔⓓ %d ⓡⓞⓦⓢ."
        self.assertEqual(expected, self.util.pseudolocalize(test_data_printffmtspec))

    def test_transliterate_fullwidth(self):
        expected = u"Ｔｈｅ ｑｕｉｃｋ ｂｒｏｗｎ ｆｏｘ ｊｕｍｐｓ ｏｖｅｒ ｔｈｅ ｌａｚｙ ｄｏｇ"
        self.util.transforms = [pseudol10nutil.transforms.transliterate_fullwidth]
        self.assertEqual(expected, self.util.pseudolocalize(self.test_data))
        test_data_fmtspec = u"Source {0} returned 0 rows, source {1} returned 1 row."
        expected = u"Ｓｏｕｒｃｅ {0} ｒｅｔｕｒｎｅｄ ０ ｒｏｗｓ, ｓｏｕｒｃｅ {1} ｒｅｔｕｒｎｅｄ １ ｒｏｗ."
        self.assertEqual(expected, self.util.pseudolocalize(test_data_fmtspec))
        test_data_printffmtspec = u"Source %(source0)s returned 0 rows, source %(source1)s returned 1 row."
        expected = u"Ｓｏｕｒｃｅ %(source0)s ｒｅｔｕｒｎｅｄ ０ ｒｏｗｓ, ｓｏｕｒｃｅ %(source1)s ｒｅｔｕｒｎｅｄ １ ｒｏｗ."
        self.assertEqual(expected, self.util.pseudolocalize(test_data_printffmtspec))
        test_data_printffmtspec = u"Source %s returned %d rows."
        expected = u"Ｓｏｕｒｃｅ %s ｒｅｔｕｒｎｅｄ %d ｒｏｗｓ."
        self.assertEqual(expected, self.util.pseudolocalize(test_data_printffmtspec))

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

    def test_simple_square_brackets(self):
        expected = u"[The quick brown fox jumps over the lazy dog]"
        self.util.transforms = [pseudol10nutil.transforms.simple_square_brackets]
        self.assertEqual(expected, self.util.pseudolocalize(self.test_data))

    def test_pad_length(self):
        expected = u"The quick brown fox jumps over the lazy dog﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘🚦﹎ЍאǆᾏⅧ㈴㋹퓛ﺏ𝟘🚦﹎Ѝ"
        self.util.transforms = [pseudol10nutil.transforms.pad_length]
        self.assertEqual(expected, self.util.pseudolocalize(self.test_data))

    def test_expand_vowels_no_vowels(self):
        test_data = u"jmpng"
        expected = u"jmpnggggggggggg"
        self.util.transforms = [pseudol10nutil.transforms.expand_vowels]
        self.assertEqual(expected, self.util.pseudolocalize(test_data))

    def test_expand_vowels_one_vowel(self):
        test_data = u"Row"
        expected = u"Rooooooow"
        self.util.transforms = [pseudol10nutil.transforms.expand_vowels]
        self.assertEqual(expected, self.util.pseudolocalize(test_data))

    def test_expand_vowels_vowel_in_placeholder(self):
        test_data_printffmtspec = u"Source %(source0)s returned 0 rows, source %(source1)s returned 1 row."
        expected = u"Sooouuurceee %(source0)s reeetuuurneeed 0 rooows, sooouuurceee %(source1)s reeetuuurneeed 1 roooow."
        self.util.transforms = [pseudol10nutil.transforms.expand_vowels]
        self.assertEqual(expected, self.util.pseudolocalize(test_data_printffmtspec))

    def test_expand_vowels_transliterated_source(self):
        test_data_printffmtspec = u"Șøüȓċê %(source0)s ȓêťüȓñêđ 0 ȓøẁš, šøüȓċê %(source1)s ȓêťüȓñêđ 1 ȓøẁ."
        expected = u"Șøøøüüüȓċêêê %(source0)s ȓêêêťüüüȓñêêêđ 0 ȓøøøẁš, šøøøüüüȓċêêê %(source1)s ȓêêêťüüüȓñêêêđ 1 ȓøøøøẁ."
        self.util.transforms = [pseudol10nutil.transforms.expand_vowels]
        self.assertEqual(expected, self.util.pseudolocalize(test_data_printffmtspec))

    def test_expand_vowels_placeholder_only(self):
        test_data_printffmtspec = u"%(source0)s"
        expected = u"%(source0)s"
        self.util.transforms = [pseudol10nutil.transforms.expand_vowels]
        self.assertEqual(expected, self.util.pseudolocalize(test_data_printffmtspec))


if __name__ == "__main__":
    unittest.main()
