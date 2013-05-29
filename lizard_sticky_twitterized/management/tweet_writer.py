#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.
from django.contrib.gis.geos import Point
from lizard_sticky_twitterized.models import StickyTweet


class TweetWriter():

    def __init__(self, tweet, limit=300):
        self.tweet = tweet
        self.limit = limit

    def store(self):
        """
        Either stores geo-coded tweets as new entries or overwrites oldest
        """
        tweet = self.tweet
        if tweet.get('coordinates') is not None:
            if self._full():
                self._store_tweet(StickyTweet.objects.order_by('created_on')[0])
            else:
                self._store_tweet(StickyTweet())

    def _store_tweet(self, new_tweet):
        tweet = self.tweet
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

    def _full(self):
        limit = self.limit-1
        if StickyTweet.objects.count() > limit:
            return True
