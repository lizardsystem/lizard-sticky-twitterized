lizard-sticky-twitterized
==========================================

This app is used to display tweets from twitter.

Development installation
------------------------

The first time, you'll have to run the "bootstrap" script to set up setuptools
and buildout::

    $> python bootstrap.py

And then run buildout to set everything up::

    $> bin/buildout

(On windows it is called ``bin\buildout.exe``).

You'll have to re-run buildout when you or someone else made a change in
``setup.py`` or ``buildout.cfg``.

The current package is installed as a "development package", so
changes in .py files are automatically available (just like with ``python
setup.py develop``).

Tests can always be run with ``bin/test`` or ``bin\test.exe``.

Using the djangoapp in a site
-----------------------------

- Add lizard_sticky_twitter to your buildout.cfg.

- Add lizard_sticky_twitter and lizard_map to the INSTALLED_APPS in your
  settings.

- set TWITTER_USERNAME and TWITTER_PASSWORD in your settings file

Make the database tables::

    $> bin/django syncdb

Add some references in your urls.py, i.e. ``(r'^', include('lizard_lizard_twitter.urls'))``.


Harvest tweets
-------------

Add to your local settings or testsettings twitter credentials:
TWITTER_USERNAME = <username>
TWITTER_PASSWORD = <password>

Add a supervisor job to your server.cfg to start "bin/django
harvest_twitter" with your keyword (escape hashtags: \#hashtag).

server.cfg::

[supervisor]
recipe = collective.recipe.supervisor
port = ${serverconfig:supervisor-port}
programs = ${buildout:bin-directory}/django harvest_twitter <keyword>
