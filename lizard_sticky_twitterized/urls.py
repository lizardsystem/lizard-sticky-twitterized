# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$',
        'lizard_sticky_twitterized.views.sticky_browser',
        name='lizard_sticky_twitterized.sticky_browser'),
    )


if settings.DEBUG:
    # Add this also to the projects that use this application
    urlpatterns += patterns('',
        (r'', include('staticfiles.urls')),
        (r'^admin/', include(admin.site.urls)),
    )
