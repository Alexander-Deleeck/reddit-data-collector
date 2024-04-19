import pandas as pd
import os
from cleaning_functions import replace_error_chars
from cleaning_functions import drop_duplicates_without_id, create_base_file
import constants

"""
1) merge ALL dataframes based on subreddit category. 
2) Remove exact duplicates
3) Remove duplicates in full_df based on 'url' and drop duplicate which has 'NaN' for 'Comments'
"""


def convert_bronze_to_silver():
    for category, main_file_name in constants.SUBREDDIT_BASE_FILE.items():
        print(f'Processing category: {category}')

        directory_path = constants.BRONZE_FOLDER + category
        if not main_file_name:
            main_df = create_base_file()
            main_file_name = category + '_full_dataset.csv'
        else:
            main_df = pd.read_csv(directory_path + '/' + main_file_name) # Make base df

        category_register = category + '_register.txt'
        for file in os.listdir(directory_path):
            print(f'{file}')
            if file != main_file_name and file != category_register :
                new_df = pd.read_csv(directory_path + '/' + file)
                main_df = pd.concat([main_df, new_df], axis=0, ignore_index=True)

        main_df = drop_duplicates_without_id(main_df)

        new_file_name = category + '_full_dataset.csv'
        main_df.to_csv(constants.SILVER_FOLDER + category + '/' + new_file_name) 
        print(f'Silver complete for: {category}\nComplete dataset has {len(main_df)} rows')

if __name__ == '__main__':
    convert_bronze_to_silver()