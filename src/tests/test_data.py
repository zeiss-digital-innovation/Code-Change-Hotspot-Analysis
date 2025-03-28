import unittest
import sys
import os

sys.dont_write_bytecode = True

import src.createHotspots as ch

class TestData(unittest.TestCase): 
#Testing the args user has given 
    #Tests not seperated by '-------------' test the same function     
    @unittest.skip("requires mocking") 
    def test_check_if_directory_exists(self):
        #TODO: Add mocking because repo does not exists on vm and other machines

        user_input: str = r"C:\Users\DITSTEIN\OneDrive - Carl Zeiss AG\Dokumente\[01] Arbeit\[01] Coding\[02] HotSpot Analyse\Code-Change-Hotspot-Analysis"
        
        path_to_repo: str = ch.check_if_directory_exists(path_to_repo=user_input)

        self.assertEqual(user_input, path_to_repo)

    def test_check_if_directory_exists_faliure(self):
        user_input: str = r"C:\this\is\a\nonexistent\path"
        
        with self.assertRaises(SystemExit) as cm:
            ch.check_if_directory_exists(path_to_repo=user_input)
            
        self.assertEqual(cm.exception.code, 1)
        
    # -------------
    def test_check_date_format(self):
        result = ch.check_date_format(date="2024-02-01")
        
        self.assertEqual(result, "2024-02-01")

    def test_check_date_format_faliure(self): 
        with self.assertRaises(SystemExit) as cm:
            ch.check_date_format(date="01/01/2024")
        
        self.assertEqual(cm.exception.code, 1)
 
#Testing if a path to a textfile containing data exists        
    # -------------    
    def test_check_if_data_exists(self):
        path_to_data: str = "src/tests/data/treemap_data.txt"
        
        check: bool = ch.check_if_data_exists(file_name=path_to_data)
        
        self.assertTrue(check)
        
    def test_check_if_data_exists_failure(self):
        path_to_nonexistent_data: str = "path/to/nonexistentdata"
        
        check: bool = ch.check_if_data_exists(file_name=path_to_nonexistent_data)
        
        self.assertFalse(check)  

#Testing the git log commands run automatically 
    @unittest.skip("requires mocking")
    def test_get_data(self):
        #TODO: Add mocking because repo does not exists on vm and other machines 

        user_input: str = r"C:\Users\DITSTEIN\OneDrive - Carl Zeiss AG\Dokumente\[01] Arbeit\[01] Coding\[02] HotSpot Analyse\Code-Change-Hotspot-Analysis"
        ch.get_data(user_input, date="2024-01-01")
        path_to_current_folder: str = os.getcwd()
        older_data_file_path: str = os.path.join(path_to_current_folder, "old.txt")
        newer_data_file_path: str = os.path.join(path_to_current_folder, "new.txt")
        result: bool = os.path.exists(older_data_file_path) and os.path.exists(newer_data_file_path)
                
        self.assertTrue(result)


        
        
