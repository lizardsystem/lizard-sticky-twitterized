#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.db import models
from django.http import HttpResponse
from django.utils import simplejson as json
from lizard_sticky_twitterized.models import StickyTweet

import logging
import urllib2
import pprint

class Command(BaseCommand):

    help = "Query Twitter's realtime search for a hashtag and store the results."
    args = "some hash tags here"
    
    def handle(self, *args, **options):
        """
        Query Twitter's realtime search for a hashtag, and store the results.
        Schedule this as needed, with something like Celery or cron.
        """
        numitems = 0
        urls = []

        if not args:
            return "No hashtags supplied.\n"
            
        for arg in args:
            urls.append("http://search.twitter.com/search.json?q=%23" + str(arg) + "&result_type=recent")
            print "- Querying Twitter for #" + str(arg)

        for url in urls:
            u = urllib2.urlopen(url)
            resultset = json.loads(u.read())
            for result in resultset['results']:
                print "*** " + unicode(result['text'])
                pprint.pprint(result)
                if not StickyTweet.objects.filter(tweet__iexact=result['text']).count() > 0:
                    tweet = StickyTweet()
                    tweet.twitter_name = result['from_user']
                    tweet.tweet = result['text']
                    tweet.status_id = result['id']
                    numitems = numitems + 1
                    if result['geo'] is not None:
                        tweet.geom = Point(
                            float(result['geo']['coordinates'][1]),
                            float(result['geo']['coordinates'][0])
                        )
                    else:
                        tweet.geom = None
                    tweet.save()
                    
        return "Added " + str(numitems) + " tweets.\n"