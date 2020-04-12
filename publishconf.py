#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://www.andrey-melentyev.com'
RELATIVE_URLS = False

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
RSS_FEED_SUMMARY_ONLY = False
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/{slug}.rss.xml'

# Additional menu items
MENUITEMS = (('Home', SITEURL),)

DELETE_OUTPUT_DIRECTORY = True

# Surely Google will survive without having data on my blog's visitors
#GOOGLE_ANALYTICS = 'UA-105911009-1'
