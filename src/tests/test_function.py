import sys
import unittest

sys.dont_write_bytecode = True

import src.createHotspots as ch


class TestFunctions(unittest.TestCase):
    
    def test_count_lines_faliure_one(self):
        with self.assertRaises(SystemExit) as cm:
            ch.count_lines("src/tests/data/old_empty.txt", "src/tests/data/new.txt")

        self.assertEqual(cm.exception.code, 1)

    def test_count_lines_faliure_two(self):
        with self.assertRaises(SystemExit) as cm:
            ch.count_lines("src/tests/data/old.txt", "src/tests/data/new_empty.txt")

        self.assertEqual(cm.exception.code, 1)
    