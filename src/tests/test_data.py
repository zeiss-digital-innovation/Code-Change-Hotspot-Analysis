import unittest
import sys
import os

sys.dont_write_bytecode = True

import src.createHotspots as ch

class TestData(unittest.TestCase): 
#Testing the args user has given 
    #Tests not seperated by '-------------' test the same function     
    @unittest.skip("requires mocking") 
    def test_directory_exists(self):
        #TODO: Add mocking because repo does not exists on vm and other machines

        user_input: str = r"C:\Users\DITSTEIN\OneDrive - Carl Zeiss AG\Dokumente\[01] Arbeit\[01] Coding\[02] HotSpot Analyse\Code-Change-Hotspot-Analysis"
        self.assertEqual(True, ch.directory_exists(path_to_repo=user_input))
    
    def test_directory_exists_faliure(self):
    #TODO: has to be rewritten
        user_input: str = r"C:\this\is\a\nonexistent\path"
        
        self.assertFalse(ch.directory_exists(path_to_repo=user_input))
        
    # -------------
    def test_date_format_correct(self):
        self.assertTrue(ch.date_format_correct(date="2024-02-01"))
        
    def test_date_format_correct_faliure(self): 
        self.assertFalse(ch.date_format_correct(date="01/01/2024"))
        
        
 
#Testing if a path to a textfile containing data exists        
    # -------------    
    def test_data_exists(self):
        path_to_data: str = "src/tests/data/treemap_data.txt"
        
        check: bool = ch.data_exists(file_path=path_to_data)
        
        self.assertTrue(check)
        
    def test_data_exists_failure(self):
        path_to_nonexistent_data: str = "path/to/nonexistentdata"
        
        check: bool = ch.data_exists(file_path=path_to_nonexistent_data)
        
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


        
        
