#!/bin/sh
# get the start date and time
start_datetime=$(date '+%m_%d_%Y_%H_%M_%S')
echo "${start_datetime} - starting spider parts"

# go to the spider directory
cd /home/umarh/ecp_scraper

# prevent click, which pipenv relies on, from freaking out to due to lack of locale info https://click.palletsprojects.com/en/7.x/python3/
export LC_ALL=en_US.utf-8

# run the spider
/home/umarh/.local/bin/pipenv run scrapy crawl parts -o "output/%(time)s_parts.json"

# get the end date and time
end_datetime=$(date '+%m_%d_%Y_%H_%M_%S')
echo "${end_datetime} - spider finished successfully"