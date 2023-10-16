import unittest
from knob.setting import *


class TestSetting(unittest.TestCase):
    def setUp(self):
        pass

    def test_preset_keys(self):
        self.assertEqual(get_setting('TEST_ENTRY_NUM'), 1)
        self.assertEqual(get_setting('TEST_ENTRY_STR'), 'abc')
        self.assertDictEqual(get_setting('TEST_ENTRY_DICT'), {"a": 1, "b": "abc"})

    def test_debug_mode(self):
        try:
            turn_off_debug()
            self.assertFalse(is_debug_on())

            turn_on_debug()
            self.assertTrue(is_debug_on())

            self.assertEqual(get_setting('TEST_ENTRY_NUM'), 1)

            set_setting("TEST_ENTRY_NUM", 2)
            self.assertEqual(get_setting('TEST_ENTRY_NUM'), 2)

            turn_off_debug()  # debugging settings should be cleared.

            self.assertEqual(get_setting('TEST_ENTRY_NUM'), 1)

            turn_on_debug()
            self.assertEqual(get_setting('TEST_ENTRY_NUM'), 1)
        finally:
            turn_off_debug()


if __name__ == '__main__':
    unittest.main()
