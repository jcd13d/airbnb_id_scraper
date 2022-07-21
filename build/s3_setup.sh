#!/bin/bash
# This script will copy the necessary files to s3
# 1 - profile (need a profile set up for each AWS account, e.g. dev and prod)
# 2 - bucket name
project_name="id_scraper"
config_dir="config"

# Rename bucket
cp ./config/config_find_listings_template.json ./config/config_find_listings.json
sed -i "s/S3_BUCKET/$2/" ./config/config_find_listings.json
# Copy main config to master configs
aws s3 cp ./config/config_find_listings.json s3://$2/master_configs/listing_indexer_configs/config_find_listings.json --profile $1

# Add running config for batch job
# Add bucket name to config
cp ./aws/batch_submit_find_listings_template.json ./aws/batch_submit_find_listings.json
sed -i "s/S3_BUCKET/$2/" ./aws/batch_submit_find_listings.json
# Copy config to s3
aws s3 cp ./aws/batch_submit_find_listings.json s3://$2/running_configs/batch_submit_find_listings.json --profile $1
