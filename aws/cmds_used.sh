# Dont run this, this is to track what I use to deploy to fargate

# create fargate cluster
aws ecs create-cluster --cluster-name fargate-cluster

# create task definition
aws ecs register-task-definition --cli-input-json file://task_def.json

# use these to find values for next command
aws ec2 describe-security-groups
aws ec2 describe-subnets
aws ec2 describe-vcps

# made log group that I put in task def
aws logs create-log-group --log-group-name  test-group-cli

# for running task on fargate cluster
aws ecs run-task --cluster test-cli-fargate --task-definition test-job-def-pub-ip --network-configuration "awsvpcConfiguration={subnets=[subnet-05ae50b3be2cd836e],securityGroups=[sg-02cd4994ba07e9848],assignPublicIp=ENABLED}" --launch-type FARGATE

# creating s3 bucket, working with s3
aws s3api create-bucket --bucket jd-s3-test-bucket9
aws s3 cp config s3://jd-s3-test-bucket9/test_configs/ --recursive
aws s3api list-objects --bucket jd-s3-test-bucket9



# USED LOCALLY DOCKER
docker buildx build --platform=linux/amd64 -t scraper-1 .

