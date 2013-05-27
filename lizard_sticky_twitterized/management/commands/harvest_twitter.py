#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.
import logging
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
import tweetstream

from lizard_sticky_twitterized.models import StickyTweet

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


class Command(BaseCommand):
    help = "Query Twitter's realtime search for a hashtag and store the results."
    args = "Some hash tags here..."

    def handle(self, *args, **options):
        """
        Query Twitter's Streaming API for a keyword, and store the results.
        Schedule this as needed, with something like Celery or cron.

        FilterStream can be used to filter on a bbox:
        Locations are a list of bounding boxes in which geotagged tweets should originate.
        The argument should be an iterable of longitude/latitude pairs.
        FilterStream("username", "password", track=words,
        ...          follow=people, locations=locations) as stream
        """
        logger.info("Listening to Twitter's Streaming API...")
        try:
            with tweetstream.FilterStream(getattr(settings, 'TWITTER_USERNAME', 'pietje'), getattr(settings, "TWITTER_PASSWORD", "pietje"), track=args) as stream:
                self.create_tweets(stream)
        except tweetstream.ConnectionError, e:
            print "Disconnected from twitter. Reason:", e.reason

    def create_tweets(self, stream):
        for tweet in stream:
            if tweet.get('coordinates') is not None:
                new_tweet = StickyTweet()
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
                new_tweet.save()
                logger.info(new_tweet.tweet)
                logger.debug('\n\nAaand listening...\n')
