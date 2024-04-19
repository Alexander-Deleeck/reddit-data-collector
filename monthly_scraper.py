import pandas as pd
import os
import json
import praw
import datetime as dt
from dotenv import load_dotenv
from scraping_functions import scrape_comments, assign_category, configure_authentication, dataframe_timestamps, logging
import constants
import time


# Configure authentication & connection to Reddit API
reddit = configure_authentication()

# Parameters for time window & number of posts
filter_time = 'month' # choose timewindow of posts: 'hour','day','week','month','year','all'
filter_limit = 10 # choose number of posts you want to scrape. Max limit is 1000

# Fill in the subreddit name(s) you want to scrape. E.g.: 'askscience'
sub_list = ['labrats']
if not sub_list:
    sub_list.append('askscience')

# Iterate over each subreddit
for sub in sub_list:
    sub_name = sub
    df_subreddit = []
    target_subreddit = reddit.subreddit(sub_name)
    counter = 0

    # Get top subreddit posts & iterate over each one
    for post in target_subreddit.top(time_filter=filter_time, limit=filter_limit):
        # Fetch full comment tree & simplified comments from post
        full_comments_data, simplified_comments_data = scrape_comments(post)

        df_subreddit.append([post.id, str(post.author), post.title, post.score, post.url, post.num_comments, #Added post.id and post.author.name for getting creator of post
                        post.selftext, post.created, simplified_comments_data])
        
        # Save the full data to a JSON file
        category = assign_category(sub_name)
        comment_file_name = sub_name + '_' + str(post.id) + '.json'

        # Check if folder for sub comments exists, make one if not
        path_comments_category = constants.COMMENT_FOLDER + category + '/'
        if not os.path.exists(path_comments_category):
            os.makedirs(path_comments_category)
        path_comments_out = path_comments_category + comment_file_name

        try: # Check if post's comments have already been archived
            with open(path_comments_out, "x") as file: # if not yet archived, store in new file
                json.dump(full_comments_data, file, indent=4)
        except FileExistsError:
            pass 

        # Counter functions as method for preventing API limit overloading
        counter = logging(counter, max_scrapes=200, timeout_seconds=180)
        print(f'Post backed up: {post.id}')
    print(f"Comments for {counter} posts from {sub_name} backed up!")

    # Save condensed data to DataFrame
    df_subreddit = pd.DataFrame(df_subreddit, columns=['post_id','author','title', 'score', 'url', 'num_comments', 'text', 'created', 'comments'])
    month = dt.date.today().strftime("%b")
    year = dt.date.today().strftime("%y")
    df_subreddit = dataframe_timestamps(df_subreddit)

    filename = sub_name + '_FULL_comments_top'+ str(counter)+'_'+ filter_time +'_'+ month + '_20' + year + '.csv'
    path_posts_out = constants.RAW_FOLDER + filename
    df_subreddit.to_csv(path_posts_out)

    print(f'Top {counter} of past timewindow {filter_time} from r/{sub_name} backed up to csv.\n{80*"="}')
    time.sleep(80)
    print('...sleeping...')

print(f"Done with processing the following subs: {*sub_list,}")
