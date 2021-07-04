import json
import os
from decimal import Decimal
import logging




def check_menu_prices(key,value):
    """
    This method checks the prices mentioned in the json. They must all be positive integers or decimals. Otherwise key and value will be ignored.
    """
    if "-" not in value:
        try:
            if str(value[0]).isdigit():
                #checking if the first character is a currency sign or number
                Decimal(value)
            else:
                Decimal(value[1:])
        except:
            #exception for non-numeric values
            print("Issue with item {}:{}".format(key, value))
            logging.info("Issue with item {}:{}".format(key, value))
            return False
        
        return True
    else:
        #negative value
        print("Issue with item {}:{} (negative value)".format(key, value))
        logging.info("Issue with item {}:{} (negative value)".format(key, value))
        return False



def check_keys_and_values(ordered_pairs):
    """
    This method raises an error if there are two "Target Price" keys with conflicting values.
    Keys like "Target price" or "target price" or "Target Price" or other variants with upper and lower case will be accepted by this check. 
    This method also checks if there is no target price key or if any of the values are negative.
    """
    d={}
    flag=False
    for key, value in ordered_pairs:

        if "target price" in key.lower():
            if check_menu_prices(key,value.strip()):
                flag = True
                #this ensures we don't get key errors later due to difference in text format.
                
                d["target price"] = value.strip()
                
            else:
                raise ValueError("Issue with \"Target Price\" value found in JSON.")
        elif key in d:
            #checking if there are multiple target price keys with conflicting values
            #if different target price keys have the same value then this error wont be raised.
            if "target price" in key.lower() and d[key]!=value.strip():
                raise ValueError("Multiple Target Price keys with conflicting values.")
        elif check_menu_prices(key,value.strip()):
            #stripping leading and trailing whitespaces before adding to dictionary.
            d[key.strip()] = value.strip()
            
    
    if not flag:
        #this is true when there is no target price key at all
        raise ValueError("No \"Target Price\" key found in JSON.")
    
    return d


def check_and_return_json(filename):
    """
    This method checks if the json file has the right format. Additionally, it calls check_keys_and_values through object_pairs_hook to check for other
    criteria mentioned in that method. 
    """
    with open(filename) as f:
        try:
            return json.load(f, object_pairs_hook=check_keys_and_values)
        except ValueError as e:
            print("Invalid JSON file or format in {}:\n {}".format(filename,e))
            logging.exception("Invalid JSON file or format in {}: {}".format(filename,e))
            return None

def check_file(filename):
    """
    check if the file given by the user is valid or not
    """
    if os.path.isfile(filename):
        return True
    else:
        return False

def check_currency(json_dict):
    """
    This method is to check if there aren't different currencies in the menu.
    """
    curreny_set = set()
    for value in json_dict.values():
        #Each value from the json has already been stripped of leading and trailing whitespaces, hence the first character is the currency
        curreny_set.add(value[0])
    
    if len(curreny_set)!=1:
        print("JSON contains different currencies: {}.\n Please use the -i or ignore argument on command line".format(curreny_set))
        logging.info("JSON contains different currencies: {}. Exiting Program".format(curreny_set))
        return False
    else:
        json_dict["_currency"] = list(curreny_set)[0]
        return True
