#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.
from django.contrib.gis.geos import Point
from lizard_sticky_twitterized.models import StickyTweet


def determine_store(tweet):
    """
    Either stores geo-coded tweets as new entries or overwrites oldest
    """
    if tweet.get('coordinates') is not None:
        if full():
            store_tweet(StickyTweet.objects.order_by('created_on')[0], tweet)
        else:
            store_tweet(StickyTweet(), tweet)


def store_tweet(new_tweet, tweet):
    new_tweet.tweet_time = tweet.get('created_at')
    new_tweet.twitter_name = tweet.get('user').get('screen_name')
    new_tweet.tweet = tweet.get('text')
    new_tweet.status_id = int(tweet.get('id'))
    new_tweet.geom = Point(
        float(tweet.get('coordinates').get('coordinates')[0]),
        float(tweet.get('coordinates').get('coordinates')[1])
    )
    media = tweet.get('entities').get('urls')
    if media:
        new_tweet.media_url = media[0]
    else:
        new_tweet.media = None
    new_tweet.save()


def full():
    limit = 300
    if StickyTweet.objects.count() > limit:
        return True
