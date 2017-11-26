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
DEFAULT_DATE_FORMAT = '%d %B %Y'
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

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'

# Appearance
THEME = 'themes/myduckingtheme'

# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'ipynb.markup',
    'sitemap'
]

MARKUP = ('md', 'ipynb')

# Python Markdown extensions configuration, see http://pythonhosted.org/Markdown/extensions/
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {},
        'markdown.extensions.toc': {},
        'markdown.extensions.tables':{},
    }
}

# IPython plugin settings
IPYNB_USE_META_SUMMARY = False
IPYNB_IGNORE_CSS = True

IGNORE_FILES += ['.ipynb_checkpoints']

# Make the processor ignore files in static/ dir
ARTICLE_EXCLUDES = ['static']

# Take advantage of the following defaults
# STATIC_SAVE_AS = '{path}'
# STATIC_URL = '{path}'
STATIC_PATHS = [
    'static',
]
# Control over the target location of the pages
EXTRA_PATH_METADATA = {
    'static/yandex_44baf762e45a6938.html': {'path': 'yandex_44baf762e45a6938.html'},
    'static/keybase.txt': {'path': 'keybase.txt'},
    'static/robots.txt': {'path': 'robots.txt'},
    'static/resume.html': {'path': 'resume.html'},
    'static/resume.css': {'path': 'resume.css'},
}

# Sitemap configuration
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.55,
        'indexes': 0.5,
        'pages': 0.45
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'daily',
        'pages': 'weekly'
    },
    'exclude': ['tag/', 'category/']
}
