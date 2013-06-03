cd #!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.
from __future__ import division, print_function

from threading import Timer
from django.conf import settings
import urllib
import urlparse
from django.utils import simplejson as json
from twitter import *
import tweetstream
from django.contrib.gis.geos import Point
from lizard_sticky_twitterized.models import StickyTweet


def search_twitter(*args, **options):
    consumer_key = 'UKLr0fV2t5uPi8DQ5B93JQ'
    consumer_secret = 'ESf7dD8BfcqPrgwdNJctNojln9hnhwGgP2PrEtqOS3k'
    access_token = '408445237-ZLnS39Glr5O30Hszg8HU7KgZs2vWpMVBlEui1Ced'
    access_secret = '9Z47HpcubCLFJJQHAbH7ws2VbSJZFrveuiBoMgj98'
    t = Twitter(auth=OAuth(access_token, access_secret, consumer_key, consumer_secret))
    search_params = dict(q="#weer", count=100, geocode="52.09,5.10,160km", result_type='recent', include_entities='1')
    tweets = t.search.tweets(**search_params)
    while tweets:
        for tweet in tweets.get('statuses'):
            writer = TweetWriter(tweet)
            writer.store()
        next_results = tweets['search_metadata'].get('next_results')
        if next_results:
            qs = next_results[1:]
            qs_dict = urlparse.parse_qs(qs, keep_blank_values=True)
            tweets = t.search.tweets(max_id=qs_dict['max_id'][0], **search_params)
        else:
            tweets = None

def listen_to_twitter(*args, **options):
    """
    Query Twitter's Streaming API for a keyword, and store the results.

    ESCAPE keywords with #'s: \#hashtag instead of #hashtag.

    FilterStream can be used to filter on a bbox:
    Locations are a list of bounding boxes in which geotagged tweets should originate.
    The argument should be an iterable of longitude/latitude pairs.
    FilterStream("username", "password", track=words,
    ...          follow=people, locations=locations) as stream
    """
    wait = 2
    with tweetstream.FilterStream(getattr(settings, 'TWITTER_USERNAME', 'pietje'), getattr(settings, "TWITTER_PASSWORD", "pietje"), track=args) as stream:
        for tweet in stream:
            if not tweet:
                print("Disconnected from twitter\nReconnect in " + str(wait) + " second(s)")
                Timer(wait, print("Attempting to reconnect")).start()
                wait = wait * wait
            elif wait > 172800:
                print("Waited two days, twitter is broken. Giving up..")
                break
            else:
                writer = TweetWriter(tweet)
                writer.store()
                wait = 2


class TweetWriter():
    """
    Stores the content of a tweet if the tweet contains coordinates.
    Overwrites old tweets when the specified storage limit has been reached (default 300).
    """
    def __init__(self, tweet, limit=3000):
        self.tweet = tweet
        self.limit = limit

    def store(self):
        """
        Either stores geo-coded tweets as new entries or overwrites oldest
        """
        tweet = self.tweet
        if tweet.get('coordinates') is not None:
            if self._full():
                self._store_tweet(StickyTweet.objects.order_by('updated_on')[0])
            else:
                self._store_tweet(StickyTweet())

    def _store_tweet(self, new_tweet):
        tweet = self.tweet
        new_tweet.twitter_name = tweet.get('user').get('screen_name')
        new_tweet.tweet = tweet.get('text')
        new_tweet.status_id = int(tweet.get('id'))
        new_tweet.geom = Point(
            float(tweet.get('coordinates').get('coordinates')[0]),
            float(tweet.get('coordinates').get('coordinates')[1])
        )
        try:
            new_tweet.media_url = tweet.get('entities').get('media')[0].get('media_url')
        except AttributeError:
            pass
        except TypeError:
            pass
        new_tweet.save()

    def _full(self):
        limit = self.limit-1
        if StickyTweet.objects.count() > limit:
            return True
