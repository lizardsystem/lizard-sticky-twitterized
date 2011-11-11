#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.db import models
from django.http import HttpResponse
from django.utils import simplejson as json

from lizard_sticky_twitterized.models import StickyTweet

from tweetstream import FilterStream

import logging
import urllib2
import pprint

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
        with FilterStream("wijgm", "kikker123", track=args) as stream:
            for tweet in stream:
                new_tweet = StickyTweet()
                new_tweet.twitter_name = tweet['user']['screen_name']
                new_tweet.tweet = tweet['text']
                new_tweet.status_id = tweet['id']
                
                if tweet['geo'] is not None:
                    new_tweet.geom = Point(
                        float(tweet['geo']['coordinates'][1]),
                        float(tweet['geo']['coordinates'][0])
                    )
                else:
                    new_tweet.geom = None

                media = tweet['entities'].get('media')
                if media:
                    new_tweet.media_url = media[0].get('media_url')

                new_tweet.save()
                logging.debug(new_tweet.tweet)
