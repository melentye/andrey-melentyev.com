#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Andrey Melentyev'
SITENAME = 'Machine Learning Engineering'
SITESUBTITLE = 'Blog by Andrey Melentyev, software engineer by day, machine learning learner by night.'
SITEURL = ''
GITHUB_URL = 'https://github.com/melentye/andrey-melentyev.com'

TIMEZONE = 'Europe/Stockholm'
DEFAULT_LANG = 'en'
DEFAULT_CATEGORY = 'misc'

PATH = 'src'
IGNORE_FILES = []

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Additional menu items
MENUITEMS = (('Home', '/'),)

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/melentye'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})_(?P<title>.*)'

# Appearance
THEME = 'themes/myduckingtheme'

# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = ['ipynb.markup']

MARKUP = ('md', 'ipynb')

# IPython plugin settings
IPYNB_USE_META_SUMMARY = False
IPYNB_IGNORE_CSS = True

IGNORE_FILES += ['.ipynb_checkpoints']
