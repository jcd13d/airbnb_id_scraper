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


aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 443188464014.dkr.ecr.us-east-1.amazonaws.com
docker buildx build --platform=linux/amd64 -t scraper-1 .
docker tag scraper-1:latest 443188464014.dkr.ecr.us-east-1.amazonaws.com/scraper-1:latest
docker push 443188464014.dkr.ecr.us-east-1.amazonaws.com/scraper-1:latest

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

aws batch submit-job --cli-input-json file://config/batch_array_job_sub.json


# chron job run every day at 1AM EST
aws events put-rule --name "daily-id-scraper-job" --schedule-expression "cron(0 5 * * ? *)"
aws events put-targets --rule "daily-id-scraper-job" --cli-input-json file://aws/eventbridge_target.json

zip ./lambda_launch_batch.zip ./lambda_launch_batch.py

aws lambda create-function --function-name trigger-id-scrapers-batch \
--zip-file fileb://lambda_launch_batch.zip --handler lambda_launch_batch.handler --runtime python3.8 \
--role arn:aws:iam::443188464014:role/lambda-batch-role --timeout 20

aws lambda update-function-code --function-name trigger-id-scrapers-batch --zip-file fileb://lambda_launch_batch.zip

aws lambda invoke --function-name trigger-id-scrapers-batch --payload '{"test": "hello"}' response.txt --cli-binary-format raw-in-base64-out

aws events put-targets --rule "daily-id-scraper-job" --cli-input-json file://aws/eventbridge_target.json

aws events list-targets-by-rule --rule "daily-id-scraper-job"
aws events remove-targets --rule "daily-id-scraper-job" --ids "daily-scraper-batch-target"

aws lambda add-permission \
--function-name trigger-id-scrapers-batch \
--statement-id datily-id-scraper-job \
--action 'lambda:InvokeFunction' \
--principal events.amazonaws.com \
--source-arn arn:aws:events:us-east-1:443188464014:rule/daily-id-scraper-job
