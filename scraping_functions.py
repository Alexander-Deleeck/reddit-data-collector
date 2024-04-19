import json
import praw
import urllib
import time
import os
import pandas as pd
from cleaning_functions import clean_comment_text
from dotenv import load_dotenv

def configure_authentication():
    load_dotenv()
    MY_SECRET = os.environ.get("MY_SECRET")
    MY_CLIENT_ID = os.environ.get('MY_CLIENT_ID')
    MY_USER_AGENT = os.environ.get('MY_USER_AGENT')
    return praw.Reddit(client_id= MY_CLIENT_ID, client_secret= MY_SECRET, user_agent= MY_USER_AGENT)


def get_comments_structure(comment):
    """Build both full and simplified JSON structures for comments and their replies in a single pass."""
    full_comment_json = {
        "comment_id": comment.id,
        "author": str(comment.author),
        "score": comment.score,
        "text": clean_comment_text(comment.body),
        "replies": []
    }
    simplified_comment_json = {
        "text": clean_comment_text(comment.body),
        "replies": []
    }

    # Recursively go down comment tree to fetch child comments from parent comment
    for reply in comment.replies:
        if isinstance(reply, praw.models.MoreComments):
            continue
        full_reply, simplified_reply = get_comments_structure(reply)
        full_comment_json["replies"].append(full_reply)
        simplified_comment_json["replies"].append(simplified_reply)

    return full_comment_json, simplified_comment_json

def scrape_comments(post):
    """Scrape all comments from a given Reddit post and return both full and simplified JSON structures."""
    post.comments.replace_more(limit=None)  # Replace all MoreComments

    full_comments_list = []
    simplified_comments_list = []
    for comment in post.comments:
        full_comment, simplified_comment = get_comments_structure(comment)
        full_comments_list.append(full_comment)
        simplified_comments_list.append(simplified_comment)

    return full_comments_list, simplified_comments_list

def assign_category(sub_name):
    if 'bio' in sub_name:
        category = 'biology'
    elif 'data' in sub_name:
        category = 'data'
    elif 'lex' in sub_name:
        category = 'lexfridman'
    elif any(term in sub_name for term in ['openai', 'localllama', 'chatgpt','mistral']):
        category = 'largelanguagemodels'
    else:
        category = sub_name
    return category


def scrape_pictures(post, save_directory):
    gallery = []
    try:
        for image in post.media_metadata.items():
            url = image[1]['p'][0]['u']
            url = url.split("?")[0].replace("preview", "i")
            gallery.append(url)

        for index, url in enumerate(gallery):
            image_file_name = str(post.id) + '_' + str(index) + ".jpg"
            file_path = os.path.join(save_directory, image_file_name)

            if not os.path.isfile(file_path): # Check if image was not already saved in directory
                urllib.request.urlretrieve(url, file_path) # Downloads image from url to specified path
            else:
                print(f"Image {image_file_name} already backed up.")

        print(f'Images for post {post.id} saved')
        return True

    except AttributeError:
        print(f'No media for post: {post.id}')
        return False
    

def dataframe_timestamps(df_subreddit):
    df_subreddit["created"] = pd.to_datetime(df_subreddit["created"], unit='s')
    df_subreddit["year"] = df_subreddit["created"].dt.year
    df_subreddit["month"] = df_subreddit["created"].dt.month
    df_subreddit["day"] = df_subreddit["created"].dt.day
    return df_subreddit


def logging(counter:int, max_scrapes:int = 150, timeout_seconds:int = 200):
    """Function for logging the number of scraped items & waiting after X scraped items to prevent API limitations.
    max_scrapes: the number of items to scrape until timeout,
    timeout_seconds: time in seconds to sleep before continuing scraping"""
    counter += 1
    if counter % 5 == 0:
        print(counter)
    if counter % max_scrapes == 0:
        print('...sleeping...')
        time.sleep(timeout_seconds)
    return counter