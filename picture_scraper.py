import praw
import os
import urllib
from cleaning_functions import assign_category
from scraping_functions import configure_authentication
from dotenv import load_dotenv
import constants

# Configure authentication & connection to Reddit API
reddit = configure_authentication()

# Parameters for time window & number of posts
filter_time = 'all' # choose timewindow of posts: 'hour','day','week','month','year','all'
filter_limit = 1000 # choose number of posts you want to scrape. Max limit is 1000

sub_name = '' # Fill in target subreddit name
if not sub_name:
    sub_name = 'chatgpt'

target_subreddit = reddit.subreddit(sub_name)
category = assign_category(sub_name)

path_pictures_category = constants.PICTURE_FOLDER + category
if not os.path_posts_out.exists(path_pictures_category):
    os.makedirs(path_pictures_category)

counter = 0
# Iterate over top posts in specified timewindow
for post in target_subreddit.top(time_filter=filter_time, limit=filter_limit):
    gallery = []
    try:
        for image in post.media_metadata.items():
            url = image[1]['p'][0]['u']
            url = url.split("?")[0].replace("preview", "i")
            gallery.append(url)

        for index, url in enumerate(gallery):
            image_file_name = str(post.id) + '_' + str(index) + ".jpg"
            file_path = os.path.join(path_pictures_category, image_file_name)
            
            if not os.path.isfile(file_path): # Check if image was not already saved in directory
                urllib.request.urlretrieve(url, file_path) # Downloads image from url to specified path
            else:
                print(f"Image {image_file_name} already backed up.\n")
            

        print(f'Images for post {post.id} saved')
        counter += 1

    except AttributeError:
        print(f'No media for post: {post.id}')
        pass

print(f'Done dowloading {counter} images from {sub_name}')


