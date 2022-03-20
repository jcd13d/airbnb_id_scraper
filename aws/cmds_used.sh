# Dont run this, this is to track what I use to deploy to fargate

# create fargate cluster
aws ecs create-cluster --cluster-name fargate-cluster

# create task definition
aws ecs register-task-definition --cli-input-json file://aws/task_def.json

# use these to find values for next command
aws ec2 describe-security-groups
aws ec2 describe-subnets
aws ec2 describe-vcps

# made log group that I put in task def
aws logs create-log-group --log-group-name  test-group-cli

# for running task on fargate cluster
aws ecs run-task --cluster test-cli-fargate --task-definition test-job-def-pub-ip --network-configuration "awsvpcConfiguration={subnets=[subnet-05ae50b3be2cd836e],securityGroups=[sg-02cd4994ba07e9848],assignPublicIp=ENABLED}" --launch-type FARGATE
aws ecs run-task --cluster test-cli-fargate --task-definition scraper-1 --network-configuration "awsvpcConfiguration={subnets=[subnet-05ae50b3be2cd836e],securityGroups=[sg-02cd4994ba07e9848],assignPublicIp=ENABLED}" --launch-type FARGATE

# creating s3 bucket, working with s3
aws s3api create-bucket --bucket jd-s3-test-bucket9
aws s3 cp config s3://jd-s3-test-bucket9/test_configs/ --recursive
aws s3api list-objects --bucket jd-s3-test-bucket9



# USED LOCALLY DOCKER
docker buildx build --platform=linux/amd64 -t scraper-1 .

# these aport from repo creation are in the console if you click on your repo for easy cp paste
# authenticate
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 033046933810.dkr.ecr.us-east-1.amazonaws.com

# create repo
aws ecr create-repository \
    --repository-name scraper-1 \
    --image-scanning-configuration scanOnPush=true \
    --region us-east-1

# tag
docker tag scraper-1:latest 033046933810.dkr.ecr.us-east-1.amazonaws.com/scraper-1:latest
# push
docker push 033046933810.dkr.ecr.us-east-1.amazonaws.com/scraper-1:latest

aws batch create-compute-environment --cli-input-json file://aws/batch_compute_envi_config.json
aws batch create-job-queue --cli-input-json file://aws/aws_batch_job_queue.json
aws batch register-job-definition --cli-input-json file://aws/aws_batch_job_def.json
aws batch submit-job --cli-input-json file://aws/submit_batch_job.json
aws batch submit-job --cli-input-json file://aws/submit_batch_job_array.json

aws s3api delete-object --bucket jd-s3-test-bucket9 --key data/reviews/part.0.parquet
aws s3 rm s3://jd-s3-test-bucket9/ --recursive --exclude "*" --include "data/reviews/*"