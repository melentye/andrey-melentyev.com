# Machine Learning Engineering

[![Build Status](https://travis-ci.org/melentye/andrey-melentyev.com.svg?branch=master)](https://travis-ci.org/melentye/andrey-melentyev.com)

A blog about software engineering in the area of machine learning, written by an engineer.

Published as [www.andrey-melentyev.com](https://www.andrey-melentyev.com)

## Prerequisites

* Have a working Python environment, optionally a virtual environment as well.
* `pip install -r requirements.txt` to get the necessary dependencies installed.
* `aws configure set preview.cloudfront true` to enable experimental CloudFront command for invalidating the caches.

## Development

* `make html` to generate the pages.
* `make devserver` to start the server which continuously regenerates and serves pages.
* `make stopserver` to shut it down.
* `make publish` to generate the public version and publish it to S3.
* `make cf_create` and `make cf_update` to setup infrastructure in AWS.
