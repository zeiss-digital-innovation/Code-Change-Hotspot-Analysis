import createHotspots as ch
import unittest

class TestFunctions(unittest.TestCase):
    
    def test_count_lines_faliure(self):
        with self.assertRaises(SystemExit) as cm:
            ch.count_lines("src/tests/data/old_empty.txt", "src/tests/data/new.txt")

        self.assertEqual(cm.exception.code, 1)
    