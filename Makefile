projectdir := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
outputdir  := $(projectdir)/out
srcdir     := $(projectdir)/src
dns_name   := andrey-melentyev.com
cf_stack   := $(subst .,-,$(dns_name))
s3_bucket  := $(dns_name)
aws_region := us-east-1

SHELL   := /bin/bash
.SHELLFLAGS := -ec

RMDIR   ?= rm -rf
PELICAN ?= pelican
AWS_CLI ?= aws

pelicanopts ?= 
DEBUG ?= 0
ifeq ($(DEBUG), 1)
	pelicanopts += -D
endif

.PHONY : html clean devserver publish cf_create cf_update cf_status

html :
	$(PELICAN) $(srcdir) -o $(outputdir) -s pelicanconf.py $(pelicanopts)

clean :
	$(RMDIR) $(outputdir)

devserver :
	$(PELICAN) -lr $(srcdir) -o $(outputdir) -s pelicanconf.py $(pelicanopts)

publish :
	$(PELICAN) $(srcdir) -o $(outputdir) -s publishconf.py $(pelicanopts) ;\
	$(AWS_CLI) s3 sync $(outputdir)/ s3://$(s3_bucket) --acl public-read --delete ;\
	CF_DIST_ID=$$($(AWS_CLI) cloudformation describe-stacks --region $(aws_region) --stack-name $(cf_stack) --query "Stacks[0].Outputs[?OutputKey=='CloudFrontDistributionId'].OutputValue" --output text) ;\
	$(AWS_CLI) cloudfront create-invalidation  --region $(aws_region) --distribution-id $$CF_DIST_ID --paths "/*"

cf_create :
	$(AWS_CLI) cloudformation create-stack  --region $(aws_region) --stack-name $(cf_stack) --template-body file://cloudformation/template.yaml --parameters ParameterKey=RootDomainName,ParameterValue=$(dns_name)

cf_update :
	$(AWS_CLI) cloudformation update-stack  --region $(aws_region) --stack-name $(cf_stack) --template-body file://cloudformation/template.yaml --parameters ParameterKey=RootDomainName,ParameterValue=$(dns_name)

cf_status :
	$(AWS_CLI) cloudformation describe-stack-events  --region $(aws_region) --stack-name $(cf_stack) --output table --query 'StackEvents[*].[LogicalResourceId,ResourceStatus,Timestamp]' --max-items 5
