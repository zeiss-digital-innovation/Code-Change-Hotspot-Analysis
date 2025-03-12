import unittest
import sys
import os

sys.dont_write_bytecode = True

import src.createHotspots as ch

class TestData(unittest.TestCase): 
    def test_check_if_path_exists(self): 
        user_input: str = r"C:\Users\DITSTEIN\OneDrive - Carl Zeiss AG\Dokumente\[01] Arbeit\[01] Coding\[02] HotSpot Analyse\Code-Change-Hotspot-Analysis"
        path_to_repo: str = ch.check_if_path_exists(user_input)

        self.assertEqual(user_input, path_to_repo)

    def test_check_date_format(self):
        result = ch.check_date_format(date="2024-02-01")
        
        self.assertEqual(result, "2024-02-01")

    def test_check_date_format_faliure(self): 
        result = ch.check_date_format(date="01/01/2024")
        
        self.assertNotEqual(result, "01/01/2024")

    def test_get_data(self):
        user_input: str = r"C:\Users\DITSTEIN\OneDrive - Carl Zeiss AG\Dokumente\[01] Arbeit\[01] Coding\[02] HotSpot Analyse\Code-Change-Hotspot-Analysis"
        ch.get_data(user_input, date="2024-01-01")
        path_to_current_folder: str = os.getcwd()
        older_data_file_path: str = os.path.join(path_to_current_folder, "old.txt")
        newer_data_file_path: str = os.path.join(path_to_current_folder, "new.txt")
        result: bool = os.path.exists(older_data_file_path) and os.path.exists(newer_data_file_path)
                
        self.assertTrue(result)
