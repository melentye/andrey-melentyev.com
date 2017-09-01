#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Andrey Melentyev'
SITENAME = 'Engineering AI'
SITEURL = ''

PATH = 'src'
TIMEZONE = 'Europe/Stockholm'
DEFAULT_LANG = 'en'
DEFAULT_CATEGORY = 'misc'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),)

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/melentye'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})_(?P<title>.*)'
