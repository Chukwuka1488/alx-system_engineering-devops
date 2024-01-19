#!/usr/bin/python3
"""
2-main
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """
    This function queries the Reddit API and returns a list containing the titles
    of all hot articles for a given subreddit. If no results are found for the
    given subreddit, the function returns None.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    if after:
        url += f"?after={after}"
    headers = {'User-Agent': 'custom'}
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        return None
    else:
        data = response.json()['data']
        hot_list.extend([post['data']['title'] for post in data['children']])
        after = data['after']
        if after is not None:
            return recurse(subreddit, hot_list, after)
        return hot_list
