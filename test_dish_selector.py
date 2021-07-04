import json
import unittest
import os
from utils_dish_selector import (check_and_return_json, check_currency, check_keys_and_values, check_menu_prices)

class TestDishSelector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #this variable contains the file path to the test files
        cls.current_folder = os.path.dirname(os.path.realpath(__file__))
        cls.test_folder = os.path.join(cls.current_folder, "test_files")
        #the following variables are paths to different test files
        cls.menu_euro = os.path.join(cls.test_folder, "menu_euro.json")
        cls.menu = os.path.join(cls.test_folder, "menu.json")
        

    def test_check_and_return_json_instance(self):
        #this method takes a json and returns a dictionary
        self.assertIsInstance(check_and_return_json(self.menu), dict, "Should be a dictionary.")
    
    def test_check_and_return_json(self):
        #this is a valid json document, should not return None
        self.assertIsNotNone(check_and_return_json(self.menu_euro), "Should not be None.")
    
    def test_check_currency(self):
        #two different currencies in the dictionary, should return False
        self.assertFalse(check_currency({"item1":"$56","item2":"€56"}), "Should be False")
    
    def test_check_keys_and_values(self):
        #ordered pairs in argument do not have "Target Price", should raise ValueError
        with self.assertRaises(ValueError):
            check_keys_and_values([("item1","$1"), ("item2","$2")])

    def test_check_menu_prices(self):
        #negative price in the menu, should return False
        self.assertFalse(check_menu_prices("item1","-$41"))
    

if __name__=="__main__":
    unittest.main()
