from pandas import DataFrame
import pandas as pd
import tabulate as tb

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    Red = '\033[91m'
    Green = '\033[92m'
    Blue = '\033[94m'
    Cyan = '\033[96m'
    White = '\33[37m'
    Yellow = '\033[93m'
    Magenta = '\033[95m'
    Grey = '\033[90m'
    Black = '\033[90m'
    Default = '\033[99m'


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'left')
pd.set_option('display.precision', 3)
pd.set_option('display.max_colwidth', None)


def print_it(title: str, data: DataFrame):
    print(f'{bcolors.HEADER} {bcolors.BOLD}  {title}')
    for record in data:
        print(f'{bcolors.White} {record}')

def print_it_line(text: str):
    print(f'{bcolors.White} {text}')

def print_it_line_title(title: str):
    print(f'{bcolors.HEADER} {bcolors.BOLD}  {title}')

def tabulate_it(title: str, data: DataFrame):
    print(f'{bcolors.HEADER} {bcolors.BOLD}  {title}')
    print(bcolors.White + tb.tabulate(data, headers='keys', tablefmt='fancy_outline', showindex="never"))

def tabulate_dict(dic_data):
    print(tb.tabulate(dic_data, headers="keys", tablefmt='fancy_outline'))
