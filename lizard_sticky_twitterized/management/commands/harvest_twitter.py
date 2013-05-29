#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.
from django.conf import settings
from django.core.management.base import BaseCommand
import tweetstream
from lizard_sticky_twitterized.management import tweet_writer


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
        try:
            with tweetstream.FilterStream(getattr(settings, 'TWITTER_USERNAME', 'pietje'), getattr(settings, "TWITTER_PASSWORD", "pietje"), track=args) as stream:
                for tweet in stream:
                    writer = tweet_writer.TweetWriter(tweet)
                    writer.store()
        except tweetstream.ConnectionError, e:
            print "Disconnected from twitter. Reason:", e.reason
            pass