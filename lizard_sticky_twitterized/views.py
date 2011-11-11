# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from lizard_map import coordinates
from lizard_map.views import AppView
from lizard_sticky_twitterized.models import StickyTweet



class StickyBrowserView(AppView):
    # hier de tweets van onderst. functie implementeren als functie
    # remco weet er meer van..
    
    def tweets(self):
        return StickyTweet.objects.filter(visible=True).order_by('-created_on')
        
    template_name = 'lizard_sticky_twitterized/sticky_twitterized-browser.html'
