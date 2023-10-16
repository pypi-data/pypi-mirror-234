from unittest import TestCase

from pycarlo.common.utils import truncate_string


class UtilsTests(TestCase):
    def test_truncate_string(self):
        self.assertEquals("abcd", truncate_string("abcde", 4))
        self.assertEquals("abñ", truncate_string("abñde", 4))
        self.assertEquals("añc", truncate_string("añcd", 4))
        self.assertEquals("abc", truncate_string("abcñe", 4))
