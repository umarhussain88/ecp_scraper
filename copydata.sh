#!/bin/sh
# copy data to azure 
start_job=$(date '+%m_%d_%Y_%H_%M_%S')
echo "${start_job} - starting upload"
azcopy cp /home/umarh/ecp_scraper/output/ "$ecp_blob_storage" --recursive 
# remove everything from src dir to keep it clean. 
start_rm=$(date '+%m_%d_%Y_%H_%M_%S')
echo "${start_rm} removing files from src"
rm -rf /home/umarh/ecp_scraper/output/*
end_job=$(date '+%m_%d_%Y_%H_%M_%S')
echo "${end_job} finished job"
