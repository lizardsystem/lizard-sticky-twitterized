#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.
import logging
import urllib2
import pprint

from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.db import models
from django.http import HttpResponse
from django.utils import simplejson as json
from tweetstream import FilterStream, SampleStream

from lizard_sticky_twitterized.models import StickyTweet


logger = logging.getLogger(__name__)


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
        ...                               follow=people, locations=locations) as stream
        """
        logger.warn("Listening to Twitter's Streaming API...")
        with FilterStream(getattr(settings, 'TWITTER_USERNAME', 'pietje'), getattr(settings, "TWITTER_PASSWORD", "pietje"), track=args) as stream:

            for tweet in stream:
                if tweet.get('coordinates', None) is not None:
                    new_tweet = StickyTweet()
                    new_tweet.twitter_name = tweet.get('user', {}).get('screen_name', "")
                    new_tweet.tweet = tweet.get('text', "")
                    new_tweet.status_id = int(tweet.get('id', ""))
                    new_tweet.geom = Point(
                        float(tweet.get('coordinates')['coordinates'][0]),
                        float(tweet.get('coordinates')['coordinates'][1])
                    )
                    media = tweet.get('entities').get('urls')
                    if media:
                        new_tweet.media_url = media[0]

                    new_tweet.save()
                    logger.warn(new_tweet.tweet)
