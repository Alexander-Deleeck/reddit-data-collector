import os
import pandas as pd
import os
import json
import datetime as dt
from scraping_functions import assign_category, configure_authentication, scrape_comments, scrape_pictures, logging, dataframe_timestamps
import constants


reddit = configure_authentication()

filter_time = 'all'
filter_limit = 1000

df_redditor = []
counter = 0

user_name = '' # Fill in the username of user whose posts you want to scrape. Eg: 'janedoe'

user = reddit.redditor(user_name)
user_posts = user.submissions.top(time_filter=filter_time, limit=filter_limit)

for index, post in enumerate(user_posts):
    if index == filter_limit:
        break

    sub_name = str(post.subreddit)
    category = assign_category(sub_name)

    path_comments_category = constants.COMMENT_FOLDER + category + '/'
    comment_file_name = sub_name + '_' + str(post.id) + '.json'
    path_comments_out = path_comments_category + comment_file_name

    # Check whether comments folder for category exists
    if not os.path.exists(path_comments_category):
        os.makedirs(path_comments_category)
    
    path_pictures_category = constants.PICTURE_FOLDER + category + '/'
    if not os.path_posts_out.exists(path_pictures_category):
        os.makedirs(path_pictures_category)

    full_comments_data, simplified_comments_data = scrape_comments(post)
    post_pictures_flag = scrape_pictures(post, path_pictures_category)

    df_redditor.append([post.id, str(post.author), post.title, post.score, post.url, post.num_comments, 
                    post.selftext, post.created, simplified_comments_data, post_pictures_flag])

    try: # Check if post's comments have already been archived
        with open(path_comments_out, "x") as file: # if not yet archived, store in new file
            json.dump(full_comments_data, file, indent=4)
    except FileExistsError:
        print(f'Post ALREADY BACKED UP: {post.id}')
        pass 

    counter = logging(counter)
    print(f'Post backed up: {post.id}')
print(f"Comments for u/{user} backed up!")

df_redditor = pd.DataFrame(df_redditor, columns=['post_id','author','title', 'score', 'url', 'num_comments', 'text', 'created', 'comments','images'])

month = dt.date.today().strftime("%b")
year = dt.date.today().strftime("%y")

filename = 'user' + '_' + user_name + '_FULL_comments_top'+ str(counter)+'_'+ filter_time+'_'+ month + '_20' + year + '.csv'

df_redditor = dataframe_timestamps(df_redditor)
path = constants.RAW_FOLDER
df_redditor.to_csv(path+filename)

print(f'Top {counter} of past timewindow {filter_time} from user {user} backed up to csv.\n{80*"="}')
