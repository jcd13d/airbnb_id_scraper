#!/bin/bash
# 1 - profile (e.g. dev or prod)
# 2 - S3 bucket name
# 3 - account number

# TODO CHANGE to be compatible with my stuff this is from george

# Create Paginated scraper policy - allows a batch to invoke another lambda
cp ./aws/InvokePaginatedScraperPolicy_document_template.json ./aws/InvokePaginatedScraperPolicy_document.json
sed -i "s/ACT_ID/$3/" ./aws/InvokePaginatedScraperPolicy_document.json
aws iam create-policy --policy-name InvokePaginatedScraperPolicy --policy-document file://aws/InvokePaginatedScraperPolicy_document.json --profile $1

# Create a role for the Batch task definition
aws iam create-role --role-name InvokePaginatedScraperRoleBatch --assume-role-policy-document file://aws/batch_trust_policy.json --profile $1
# Assign permissions to role
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess --role-name InvokePaginatedScraperRoleBatch --profile $1
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonECS_FullAccess --role-name InvokePaginatedScraperRoleBatch --profile $1
aws iam attach-role-policy --policy-arn arn:aws:iam::$3:policy/InvokePaginatedScraperPolicy --role-name InvokePaginatedScraperRoleBatch --profile $1

# Create log group
aws logs create-log-group --log-group-name find-listings-batch-log-group --profile $1

# Add account id to job defition config
cp ./aws/register_job_definition_template.json ./aws/register_job_definition.json
sed -i "s/ACT_ID/$3/" ./aws/register_job_definition.json
# Add s3 bucket to job definition config
sed -i "s/S3_BUCKET/$2/" ./aws/register_job_definition.json

aws batch register-job-definition --cli-input-json file://aws/register_job_definition.json --profile $1
aws batch create-job-queue --cli-input-json file://aws/batch_job_queue.json --profile $1
