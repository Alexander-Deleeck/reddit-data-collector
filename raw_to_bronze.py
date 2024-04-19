import pandas as pd
import re
import os
from cleaning_functions import replace_error_chars
from cleaning_functions import write_to_file
from cleaning_functions import assign_category
import constants

"""The goal of this script is to replace faulty characters in all of the datasets &
subsequently copy the cleaned versions to the silver layer"""

def convert_raw_to_bronze():
    counter = 0
    
    for file in os.listdir(constants.RAW_FOLDER):
        counter += 1
        print(f'Now processing: {file}')
        category = assign_category(file)        

        filepath = constants.RAW_FOLDER + '/' + file
        df = pd.read_csv(filepath)

        df.drop('Unnamed: 0', axis=1, inplace=True)
        df = replace_error_chars(df)

        register_name = category + '_register.txt'
        register_path = constants.BRONZE_FOLDER + '/' + category + '/' + register_name
        write_to_file(register_path, file)

        path_to_bronze = constants.BRONZE_FOLDER + '/' + category + '/' + file
        df.to_csv(path_to_bronze)
        print(f'{counter}){category}: done\n')

if __name__ == "__main__":
    convert_raw_to_bronze()
