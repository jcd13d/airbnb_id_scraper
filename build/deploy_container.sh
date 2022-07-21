#!/bin/bash
# 1 - profile (e.g. dev or prod)
# 2 - S3 bucket name
# 3 - account number
project_name="id-scraper-test"

aws ecr create-repository --repository-name "${project_name}" --profile $1

aws ecr get-login-password --region us-east-1 --profile $1 | docker login --username AWS --password-stdin $3.dkr.ecr.us-east-1.amazonaws.com
docker buildx build --platform=linux/amd64 -t "${project_name}" .
docker tag "${project_name}":latest $3.dkr.ecr.us-east-1.amazonaws.com/"${project_name}":latest
docker push $3.dkr.ecr.us-east-1.amazonaws.com/"${project_name}":latest