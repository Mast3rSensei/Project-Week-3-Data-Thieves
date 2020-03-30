import pandas as pd
import numpy as np
import praw

reddit = praw.Reddit('api_scavenger', user_agent='python:api_scavenger:v0.1 (by u/poisson_89)')
subreddit = reddit.subreddit('reddeadredemption')
submissions = list(subreddit.hot(limit=5))
print(submissions[0].title)
