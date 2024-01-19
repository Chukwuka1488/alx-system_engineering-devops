#!/usr/bin/python3
"""
100-main
"""
import requests
from collections import Counter


def count_words(subreddit, word_list, after=None, word_count=Counter()):
    """
    This function queries the Reddit API, parses the title of all hot articles,
    and prints a sorted count of given keywords.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    if after:
        url += f"?after={after}"
    headers = {'User-Agent': 'custom'}
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        return
    else:
        data = response.json()['data']
        for post in data['children']:
            title = post['data']['title'].lower().split()
            word_count += Counter(word for word in title if word in word_list)
        after = data['after']
        if after is not None:
            return count_words(subreddit, word_list, after, word_count)
        word_count = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
        for word, count in word_count:
            print(f"{word}: {count}")
