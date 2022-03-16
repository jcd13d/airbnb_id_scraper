aws ecs create-cluster --cluster-name fargate-cluster

aws ecs register-task-definition --cli-input-json file://task_def.json

# use these to find values for next command
aws ec2 describe-security-groups
aws ec2 describe-subnets
aws ec2 describe-vcps
# made log group that I put in task def
aws logs create-log-group --log-group-name  test-group-cli

aws ecs run-task --cluster test-cli-fargate --task-definition test-job-def-pub-ip --network-configuration "awsvpcConfiguration={subnets=[subnet-05ae50b3be2cd836e],securityGroups=[sg-02cd4994ba07e9848],assignPublicIp=ENABLED}" --launch-type FARGATE




