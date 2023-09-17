# utils/reddit_utils.py

import praw
import json

def reddit_obj():

    with open('json-files/credentials.json') as f:
        data = json.load(f)

    user_values = data["api_credentials"]

    reddit = praw.Reddit(
        client_id=user_values['client_id'],
        client_secret=user_values['client_secret'],
        user_agent = user_values['user_agent'],
        password=user_values['password'],
    )

    return reddit