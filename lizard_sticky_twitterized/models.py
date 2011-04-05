# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import datetime

from django.contrib.auth.models import User
from django.contrib.gis.db import models


class StickyTweet(models.Model):
    """
    StickyTweet
    """
    twitter_name = models.CharField(blank=True, max_length=255)
    status_id = models.PositiveIntegerField(blank=True, null=True, max_length=255)
    tweet = models.CharField(blank=True, max_length=255)
    visible = models.BooleanField(default=True, help_text=u"Defines the site-wide visibility of the tweet")
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return u'%s' % self.tweet

