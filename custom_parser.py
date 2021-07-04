import argparse
import sys

class CustomParser(argparse.ArgumentParser):
    """
    This custom parser is used to prevent argparse from printing error messages and presenting them
    as information when the user makes a mistake while using command line arguments.
    """
    def error(self,message:str)->None:
        sys.stderr.write('{}\n'.format(message))
        self.print_help()
        sys.exit(2)
    