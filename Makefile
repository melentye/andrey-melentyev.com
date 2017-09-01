projectdir := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
outputdir  := $(projectdir)/out
srcdir     := $(projectdir)/src
s3_bucket  := engineering-ai

SHELL    = /bin/sh
MKDIR_P ?= mkdir -p
RMDIR   ?= rm -rf
PYTHON  ?= python
PELICAN ?= pelican
AWS     ?= aws

pelicanopts ?= 
DEBUG ?= 0
ifeq ($(DEBUG), 1)
	pelicanopts += -D
endif

.PHONY : all, site, html, serve, publish, s3_upload, clean 

all : site

site : html

$(outputdir) :
	$(MKDIR_P) $@

html : $(pages) $(outputdir)
	$(PELICAN) $(srcdir) -o $(outputdir) -s pelicanconf.py $(pelicanopts)

serve :
	cd $(outputdir) && $(PYTHON) -m pelican.server

publish:
	$(PELICAN) $(srcdir) -o $(outputdir) -s publishconf.py $(pelicanopts)

s3_upload: publish
	$(AWS) s3 sync $(outputdir)/ s3://$(s3_bucket) --acl public-read --delete

clean :
	$(RMDIR) $(outputdir)
