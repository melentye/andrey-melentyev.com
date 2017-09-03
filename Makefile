projectdir := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
outputdir  := $(projectdir)/out
srcdir     := $(projectdir)/src
dns_name   := andrey-melentyev.com
cf_stack   := $(subst .,-,$(dns_name))
s3_bucket  := $(dns_name)


SHELL   := /bin/bash
.SHELLFLAGS := -ec

MKDIR_P ?= mkdir -p
RMDIR   ?= rm -rf
PYTHON  ?= python
PELICAN ?= pelican
AWS_CLI ?= aws

pelicanopts ?= 
DEBUG ?= 0
ifeq ($(DEBUG), 1)
	pelicanopts += -D
endif

.PHONY : all site html serve publish s3_upload cf_create cf_update cf_status clean

all : site

site : html

$(outputdir) :
	$(MKDIR_P) $@

html : $(pages) $(outputdir)
	$(PELICAN) $(srcdir) -o $(outputdir) -s pelicanconf.py $(pelicanopts)

serve :
	cd $(outputdir) && $(PYTHON) -m pelican.server

publish :
	$(PELICAN) $(srcdir) -o $(outputdir) -s publishconf.py $(pelicanopts) ;\
	$(AWS_CLI) s3 sync $(outputdir)/ s3://$(s3_bucket) --acl public-read --delete ;\
	CF_DIST_ID=$$($(AWS_CLI) cloudformation describe-stacks --stack-name $(cf_stack) --query "Stacks[0].Outputs[?OutputKey=='CloudFrontDistributionId'].OutputValue" --output text) ;\
	$(AWS_CLI) cloudfront create-invalidation --distribution-id $$CF_DIST_ID --paths "/*"

cf_create :
	$(AWS_CLI) cloudformation create-stack --stack-name $(cf_stack) --template-body file://cloudformation/template.yaml --parameters ParameterKey=RootDomainName,ParameterValue=$(dns_name)

cf_update :
	$(AWS_CLI) cloudformation update-stack --stack-name $(cf_stack) --template-body file://cloudformation/template.yaml --parameters ParameterKey=RootDomainName,ParameterValue=$(dns_name)

cf_status :
	$(AWS_CLI) cloudformation describe-stack-events --stack-name $(cf_stack) --output table --query 'StackEvents[*].[LogicalResourceId,ResourceStatus,Timestamp]' --max-items 5

clean :
	$(RMDIR) $(outputdir)
