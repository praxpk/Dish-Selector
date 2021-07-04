import argparse
import logging
from custom_parser import CustomParser
import textwrap
import time
from collections import deque, defaultdict
from decimal import Decimal
from utils_dish_selector import (check_currency, check_and_return_json, check_file)


def select_from_menu(target_price,menu_list):
    """
    This is the main algorithm that generates the different combinations equal to the target price.
    Using an iterative approach (BFS) instead of a recursive one.
    """
    q = deque()
    #we append a tuple to the que, each tuple consists of the dishes, an index and the total cost of those dishes.
    #The dishes in the tuple exist from 0 to the index in the menu_list
    q.append(([],0,0))
        
    result = set()
        
    N = len(menu_list)

    while(q):
        dishes, index, cost_so_far = q.popleft()
        if cost_so_far == target_price:
            result.add(tuple(dishes))
        elif cost_so_far<target_price:
            for i in range(index,N):
                #iterate from the index to the end of the list and add each dish's price to the cost so far to
                # see if it is lower than or equal to the target price.
                if cost_so_far+menu_list[i][0]<=target_price:
                    q.append((dishes+[menu_list[i]],i,cost_so_far+menu_list[i][0]))
    
    return list(result)

def get_menu_as_list(json_dict):
    """
    Takes in the json and converts it into a list of tuples where each tuple consists of (price of item, name of item)
    The reason for using round is because we need floor values.
    In menus, one would not have 0.001 dollar or pound or euros (There might be other currencies but for simiplicity rounding off to two).
    Hence, if the the price is $2.679 we need $2.67 which round achieves.
    """
    menu_list = []
    for key, value in json_dict.items():
        if str(value[0]).isdigit():
            item_value = round(Decimal(value),2)
            menu_list.append((item_value,key))
        else:
            item_value = round(Decimal(value[1:]),2)
            menu_list.append((item_value,key))

        
    
    menu_list.sort()
    
    return menu_list

def print_final_selection(item,currency):
    """
    The final result is returned by the algorithm as a list of lists. This method takes an individual list and prints in a format.
    """
    item_freq = defaultdict(int)
    for i in item:
        #each item is a tuple => (price, item name)
        item_freq[i]+=1

    for i in item_freq:
        print("\tItem: {}, price: {}{}, quantity: {}".format(i[1],str(currency or ''),i[0],item_freq[i]))
    


def main():
    #Using custom parser class to prevent the word "error" from being printed on command line.
    parser = CustomParser(description="This program takes a menu present in a json file and returns dishes that can be purchased for a target price.", 
    formatter_class=argparse.RawTextHelpFormatter)
    #using RawTextHelpFormatter and Textwrap to ensure help text is printed line by line. Using \n does not work in argpase help.
    parser.add_argument("-m","--menu",required=True,help=textwrap.dedent("""\
        Enter the name of the JSON file that contains the menu.
        If the file is not in the same folder as the python file, provide full path.
        Example: python dish_selector.py -m my_menu.json\n\
        Example: python dish_selector.py -m /home/user/Documents/menu.json    """))

    parser.add_argument('-i','--ignore', action='store_true',help=textwrap.dedent("""\
        Use this option to ignore currency characters altogether.
        Do not provide any arguments after -i.
        Example: python dish_selector.py menu my_menu.json -i
        """))
    args = vars(parser.parse_args())
    
    logging.info("Arguments provided by user: {}".format(args))
    
    #checking if file is valid
    if not check_file(args['menu']):
        logging.info("Filename provided by user does not exist: {}".format(args["menu"]))
        print("File {} does not exist. Please check the file name or file path.".format(args["menu"]))
        return

    json_doc = check_and_return_json(args['menu'])
    
    if not json_doc:
        #the check_and_return_json method returns None if the format is incorrect
        return

    if not args["ignore"] and not check_currency(json_doc):
        #check currency returns False if there are multiple currencies in the menu
        return
    
    target_price = json_doc.pop("target price")
    if str(target_price[0]).isdigit():
        # check comments in method get_menu_as_list(json_dict) for explanantion on using round.
        target_price = round(Decimal(target_price),2)
    else:
        target_price = round(Decimal(target_price[1:]),2)

    currency = None
    if not args["ignore"]:
        currency = json_doc.pop("_currency")

    menu_as_list = get_menu_as_list(json_doc)
    
    logging.info("Target price: {},  Menu as list: {}, currency: {}".format(target_price, menu_as_list, str(currency or '')))

    selection =  select_from_menu(target_price,menu_as_list)

    

    if len(selection)==0:
        print("No combination of dishes for given target price: {}{}".format(str(currency or ''),target_price))
    else:
        print("The following combinations can be purchased with the given target price: {}{}".format(str(currency or ''),target_price))
        logging.info("Result:")
        for i in range(len(selection)):
            print('Selection {}:'.format(i+1))
            logging.info("Selection {}:{}".format(i+1,selection[i]))
            print_final_selection(selection[i],currency)
        



if __name__=="__main__":
    logging.basicConfig(filename='dish_selector.log', level=logging.INFO)
    logging.info("*"*100) #acts as a visual separator between two different executions.
    logging.info("Program execution started, {}".format(time.ctime(time.time())))
    main()  
    logging.info("Program execution ended, {}".format(time.ctime(time.time())))    
    logging.info("*"*100)



