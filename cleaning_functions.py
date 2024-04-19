import pandas as pd
import re
import os
import constants

def create_base_file():
    df_base = pd.DataFrame(columns=['post_id','author','title', 'score', 'url', 'num_comments', 'text', 'created', 'comments', 'year', 'month', 'day'])
    return df_base


def replace_error_chars(df: pd.DataFrame):
    df.replace({'’': "'"}, regex=True, inplace=True) # replaces curly apostrophe
    df.replace({'“': '"'}, regex=True, inplace=True) # replaces double left curly apostrophe
    df.replace({'”': '"'}, regex=True, inplace=True) # replaces double right curly apostrophe
    df.replace({'\*\*': ""}, regex=True, inplace=True) # removes double **
    return df

def clean_comment_text(text):
    # Replacing characters
    text = text.replace("’", "'")
    text = text.replace("“", "\"")
    text = text.replace("”", "\"")
    # Removing characters
    text = text.replace("**", "")
    return text

def drop_duplicates_without_comments(main_df):
    main_df.drop_duplicates(inplace=True)
    main_df = main_df.sort_values(['url', 'comments']).drop_duplicates(['url'], keep='first') # This drops the duplicates which have NaN for comments col
    return main_df

def drop_duplicates_without_id(main_df):
    main_df.drop_duplicates(subset=['post_id', 'author', 'url', 'comments'], inplace=True) # Drop exact duplicates (for newer files)
    main_df = main_df.sort_values(['url', 'post_id', 'comments']).drop_duplicates(['url'], keep='first') # This drops the duplicates which have NaN for post_id col
    return main_df

# Not implemented yet
def write_to_file(file_path, file_name):
    # Check if the file exists
    file_exists = os.path.isfile(file_path)
    
    # Open the file in append mode if it exists, or write mode if it doesn't
    with open(file_path, 'a' if file_exists else 'w') as file:
        # Write the variable name on a new line
        file.write(file_name + '\n')


