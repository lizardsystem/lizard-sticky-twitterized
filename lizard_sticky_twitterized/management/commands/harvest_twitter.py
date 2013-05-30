#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.
from __future__ import division, print_function

from django.conf import settings
from django.core.management.base import BaseCommand
import tweetstream
from lizard_sticky_twitterized.management import tweet_writer

from threading import Timer


class Command(BaseCommand):
    help = "Query Twitter's realtime search for a hashtag and store the results."
    args = "Some hash tags here..."
    overwrite = False

    def handle(self, *args, **options):
        """
        Query Twitter's Streaming API for a keyword, and store the results.

        ESCAPE keywords with #'s: \#hashtag instead of #hashtag.

        FilterStream can be used to filter on a bbox:
        Locations are a list of bounding boxes in which geotagged tweets should originate.
        The argument should be an iterable of longitude/latitude pairs.
        FilterStream("username", "password", track=words,
        ...          follow=people, locations=locations) as stream
        """
        wait = 1
        with tweetstream.FilterStream(getattr(settings, 'TWITTER_USERNAME', 'pietje'), getattr(settings, "TWITTER_PASSWORD", "pietje"), track=args) as stream:
            for tweet in stream:
                if not tweet:
                    print("Disconnected from twitter\nReconnect in " + str(wait) + " second(s)")
                    Timer(wait, lambda: print("Attempting to reconnect")).start()
                    wait = wait*10
                else:
                    writer = tweet_writer.TweetWriter(tweet)
                    writer.store()
                    wait = 1
