import sys, os
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

    def test_count_lines_older(self):
        older_data_output_file_path, newer_data_output_file_path = ch.count_lines(
            older_data_file_path="src/tests/data/old.txt", newer_data_file_path="src/tests/data/new.txt"
        )

        check_older:bool = os.path.exists(older_data_output_file_path) and os.stat(older_data_output_file_path).st_size > 0
        if check_older:
            self.assertTrue(check_older)
        else: 
            self.assertTrue(check_older, f"{older_data_output_file_path} might be non existent or empty!")

    def test_count_lines_newer(self):
        older_data_output_file_path, newer_data_output_file_path = ch.count_lines(
            older_data_file_path="src/tests/data/old.txt", newer_data_file_path="src/tests/data/new.txt"
        )

        check_older:bool = os.path.exists(newer_data_output_file_path) and os.stat(newer_data_output_file_path).st_size > 0
        if check_older:
            self.assertTrue(check_older)
        else: 
            self.assertTrue(check_older, f"{newer_data_output_file_path} might be non existent or empty!")

    def test_compare_data(self):
        treemap_data_file_path: str = ch.compare_data(
            older_data_counted_file_path="src/tests/data/older_counted.txt", newer_data_counted_file_path="src/tests/data/newer_counted.txt"
        )
        check: bool = os.path.exists(treemap_data_file_path) and os.stat(treemap_data_file_path).st_size != 0
        self.assertTrue(check)
    @unittest.skip("requires mocking")
    def test_displaying_treemap(self):
        #TODO implement mocking or refactor so it does not get displayed
        try: 
            ch.displaying_treemap(treemap_data_file_path="src/tests/data/treemap_data.txt")
            
        except Exception as e: 
            self.fail(f"An exception was raised by displaying_treemap:\n{e}")
        
        self.assertTrue(True, "No exception was raised. Check your browser.")
    