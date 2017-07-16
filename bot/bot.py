# -*- coding: UTF-8 -*-
import os
import random
import json
import re
from datetime import datetime, timedelta

from twitter import Twitter, OAuth
from BeautifulSoup import BeautifulSoup

from config import TWITTER, BASE_FOLDER, BASE_URL


def twitter_login(config_file):
    with open(config_file) as f:
        config = json.load(f)

    return Twitter(auth=OAuth(
        TWITTER["token"],
        TWITTER["token_key"],
        TWITTER["con_secret"],
        TWITTER["con_secret_key"]
    ))


def choose_random_file(base_folder):
    """ chooses a random file and returns its path """
    list = os.listdir(base_folder)
    return random.choice(list)


def extract_title(html_string):
    """ given an html file, return its title """
    soup = BeautifulSoup(html_string)
    return unicode(soup.h1.a.contents[0])


def extract_date(html_string):
    g1 = re.search('hai (\d+) días', html_string)
    if g1:
            days = timedelta(days=int(g1.group(1)))
            date_gap = datetime(2016, 3, 31) - days
            return date_gap.strftime("%d-%m-%Y")
    else:
            g1 = re.search('> o (\d+-\d+-\d+)', html_string)
            if g1:
                    return g1.group(1)
            else:
                    return ""


def compose_tweet(title, news_date, filename="", url=False):
    title_space = 140 - 23 - 10 - 2 - 2 - 4

    if len(title) > title_space:
            title = "{}...".format(title[0:title_space])

    url = url or BASE_URL.format(filename)
    return u"[{}] {} {}".format(news_date, title[0:120], url)


def tweet(t):
    filename = choose_random_file(BASE_FOLDER)

    # open the file
    with open("{}/{}".format(BASE_FOLDER, filename)) as f:
        contents = f.read()

    title = extract_title(contents)
    news_date = extract_date(contents)

    tweet = compose_tweet(title, news_date, filename)
    t.statuses.update(status=tweet)
    print(tweet)


if __name__ == "__main__":
    tweet(twitter_login)
