#!/bin/sh
# copy data to azure
start_job=$(date '+%m_%d_%Y_%H_%M_%S')
trg_dir="${ecp_blob_storage}"
src_dir="/home/umarh/ecp_scraper/output/*"
echo "Starting upload of files from ${src_dir} to blob storage"
/home/umarh/azcopy/azcopy cp /home/umarh/ecp_scraper/output/* "${trg_dir}" --recursive
#remove everything from src dir to keep it clean.
start_rm=$(date '+%m_%d_%Y_%H_%M_%S')
echo "${start_rm} removing files from src"
rm -rf /home/umarh/ecp_scraper/output/*
end_job=$(date '+%m_%d_%Y_%H_%M_%S')
echo "${end_job} finished job"
