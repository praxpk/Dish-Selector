# Dish Selector

## _Help You Select Dishes from a Menu for a Given Price_

This program presents a user with dishes they can buy from a menu for a given target price.
The menu must exist in a json file with one of the keys being "Target Price". Here is an example of the JSON file format:

>{
>   "Target price": "$15.05",
>   "mixed fruit": "$2.15",
>   "french fries": "$2.75",
>   "side salad": "$3.35",
>   "hot wings": "$3.55",
>   "mozzarella sticks": "$4.20",
>   "sampler plate": "$5.80" 
>  }

## Execution 

This program requires Python 3.x. All the libraries used in this program are present in Python standard library. 

To run this program, download the program files to a folder, use the command line, run dish_selector.py and type in the required arguments. 

### Here are the accepted arguments:

- -m or --menu : This argument is for the json file which contains the menu in the format shown above.
- -i or --ignore : This argument is to ignore currencies mentioned in the menu (or use a menu file that has no currencies).
- -h --help : Presents the help menu, has some examples on how to run the program from command line.

### Here are some examples
To get results from a json file called menu.json that exists in the same folder as dish_selector.py
```sh
python dish_selector.py -m menu.json
```

To get results from a json file called menu.json that exists in the folder /home/user/Downloads
```sh
python dish_selector.py -m /home/user/Downloads/menu.json
```

To get results from a json file while ignoring the currencies present in the json (or for json menu files that do not have currency).
```sh
python dish_selector.py -m menu.json -i
```

## Development
This module contains the following files:

- dish_selector.py: Contains the main method and the algorithm that generates the list of dishes.
- custom_parser.py: Allows to customize arparse
- utils_dish_selector.py: Contains methods that check json data before processing it. 
- test_dish_selector.py: This has test cases (unittest module) to test different methods.
- menu.json: A test input file.

## Testing
Test cases are present in test_dish_selector.py. A setUpClass method in the test class allows one to create class variables specific to testing. 

To run the test cases:
```sh
python test_dish_selector.py
```
The folder test_files contains files that are used for testing. A path variable to this folder has been created in the setUpClass method. Create test files and use os.path.join to run tests on files. 

## Logging
Upon running the program for the first time, a log file called dish_selector.log will be created. 
