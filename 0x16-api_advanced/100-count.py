#!/usr/bin/python3
"""
Show number of occurrences of keywords in hot post titles (case-insensitive)
"""
import re
import requests

API = 'https://www.reddit.com/r/{}/hot.json'


def count_words(subreddit, wordlist, nums=None, after=None):
    """
    Query reddit for hot posts and print total occurrences of each keyword
    """
    r = requests.get(
        API.format(subreddit),
        headers={'User-Agent': 'Mozilla/5.0'},
        params={'after': after, 'limit': 100},
        allow_redirects=False,
    )
    if r.status_code == 200:
        nums = nums or dict.fromkeys(wordlist, 0)
        data = r.json()['data']
        page = [word for post in data['children']
                for word in post['data']['title'].split()]
        for key in wordlist:
            for word in page:
                if key.casefold() == word.casefold():
                    nums[key] += 1
        if data['after'] is None:
            keys = sorted(filter(nums.get, nums), key=lambda k: (-nums[k], k))
            for key in keys:
                print('{}: {}'.format(key, nums[key]))
        else:
            count_words(subreddit, wordlist, nums, data['after'])
