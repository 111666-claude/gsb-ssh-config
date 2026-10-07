import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sshconf import core

TEXT = "Host web\n  User alice\n  Port 2222\n"


class SshConfigTest(unittest.TestCase):
    def test_value_found(self):
        config = core.parse(TEXT, {}, core.Counter())
        self.assertEqual(config.get("web", "User", core.Counter()), "alice")

    def test_missing_key(self):
        config = core.parse(TEXT, {}, core.Counter())
        self.assertEqual(config.get("web", "Nope", core.Counter()), "")

    def test_missing_host(self):
        config = core.parse(TEXT, {}, core.Counter())
        self.assertEqual(config.get("other", "User", core.Counter()), "")

    def test_block_count(self):
        config = core.parse(TEXT, {}, core.Counter())
        self.assertEqual(len(config.blocks), 1)

    def test_option_count(self):
        config = core.parse(TEXT, {}, core.Counter())
        self.assertEqual(len(config.blocks[0].options), 2)

    def test_counter_counts(self):
        counter = core.Counter()
        core.parse(TEXT, {}, counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
