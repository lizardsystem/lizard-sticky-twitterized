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





# def sticky_browser(
#     request,
#     template='lizard_sticky_twitterized/sticky_twitterized-browser.html',
#     crumbs_prepend=None):
#     """Show sticky browser.
# 
#     Automatically makes new workspace if not yet available
# 
#     """
#     if crumbs_prepend is not None:
#         crumbs = list(crumbs_prepend)
#     else:
#         crumbs = [{'name': 'home', 'url': '/'}]
#     crumbs.append(
#         {'name': 'meldingen',
#          'url': reverse('lizard_sticky_twitterized.sticky_browser')})
# 
#     tweets = StickyTweet.objects.filter(visible=True).order_by('-created_on')[:5]
# 
#     return render_to_response(
#         template,
#         {'javascript_hover_handler': 'popup_hover_handler',
#          'javascript_click_handler': 'sticky_popup_click_handler',
#          'tweets': tweets,
#          'crumbs': crumbs,
#          },
#         context_instance=RequestContext(request))
