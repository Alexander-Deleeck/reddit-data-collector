import os
import timeit

import pandas as pd
import re
import os
import json
import praw
import datetime as dt
from praw.models import MoreComments
from scraping_functions import scrape_comments, assign_category, scrape_pictures, dataframe_timestamps, configure_authentication, logging
import constants
import time

# Configure authentication & connection to Reddit API
reddit = configure_authentication()
# Parameters for time window & number of posts
filter_time = 'all' # choose timewindow of posts: 'hour','day','week','month','year','all'
filter_limit = 1000 # choose number of posts you want to scrape. Max limit is 1000

# Fill in target subreddit name
sub_name = '' 
if not sub_name:
    sub_name = 'chatgpt'

# Write queries or different forms of the query in this list
queries = [] 
if not queries:
    queries.append('prompt')

counter = 0
target_subreddit = reddit.subreddit(sub_name)
category = assign_category(sub_name)

path_pictures_category = save_directory = constants.PICTURE_FOLDER + category
if not os.path_posts_out.exists(path_pictures_category):
    os.makedirs(path_pictures_category)

for q in queries:
    df_query = []

    for post in reddit.subreddit(sub_name).search(q, sort='top',time_filter='all', limit=filter_limit):
        post_pictures_flag = scrape_pictures(post, path_pictures_category)

        path_comments_category = constants.COMMENT_FOLDER + category + '/'
        comment_file_name = sub_name + '_' + str(post.id) + '.json'
        path_comments_out = path_comments_category + comment_file_name

        # Check whether comments folder for category exists
        if not os.path.exists(path_comments_category):
            os.makedirs(path_comments_category)

        # Check that post's comments have not previously been archived
        if not os.path.isfile(path_comments_out):
            full_comments_data, simplified_comments_data = scrape_comments(post)

            df_query.append([post.id, str(post.author), post.title, post.score, post.url, post.num_comments,
                            post.selftext, post.created, simplified_comments_data, post_pictures_flag])

            try: # Store the comments as json file
                with open(path_comments_out, "x") as file:
                    json.dump(full_comments_data, file, indent=4)
            except FileExistsError:
                pass 
            
            counter = logging(counter)
            print(f'Post backed up: {post.id}')
        else:
            print(f'Post ALREADY BACKED UP: {post.id}')
    print(f"Comments for {q} from {counter} posts in {sub_name} backed up!")

    df_query = pd.DataFrame(df_query, columns=['post_id','author','title', 'score', 'url', 'num_comments', 'text', 'created', 'comments','images'])
    df_query = dataframe_timestamps(df_query)

    month = dt.date.today().strftime("%b")
    year = dt.date.today().strftime("%y")

    filename = q + '_' + sub_name + '_FULL_comments_top'+ str(counter)+'_'+ filter_time+'_'+ month + '_20' + year + '.csv'

    path_posts_out = constants.RAW_FOLDER + filename
    df_query.to_csv(path_posts_out)

    print(f'Top {counter} posts of past timewindow {filter_time} from query {q} in r/{sub_name} backed up to csv.\n')

print(f'The following queries were backed up: {*queries,}\n{80*"="}')