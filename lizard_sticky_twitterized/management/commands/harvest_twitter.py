#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.
from django.core.management.base import BaseCommand
from lizard_sticky_twitterized.twitter_connector import listen_to_twitter


class Command(BaseCommand):
    help = "Query Twitter's realtime search for a hashtag and store the results."
    args = "Some hash tags here..."

    def handle(self, *args, **options):
        listen_to_twitter(*args, **options)
