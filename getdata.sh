#!/bin/bash

cd eurocarparts
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl parts -o '%(time)s_parts.json'