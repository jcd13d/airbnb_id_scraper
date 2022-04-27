# airbnb_id_scraper

# Setup
* Create ECR repo
* Build container
* Push
* Update batch envi config VPC info
* Create batch environment
* Create batch job queue
* Update batch job def
* Register batch job definition
* Create recurring rule
* Create target, add to rule
  * had to use UI to create ARN from EventBridge UI

# Usage
The ID based scraper is intended to be run as a docker container in AWS Batch. The scraper
takes a list of Airbnb unique listing IDs and iterates through them to scrape the information
as configured. As of 2022/04/19 that consists of availability and pricing data. 

There are multiple configurations that are used to control the scrapers. They are listed below:
* [config_occ.json](./config/config_occ.json)
  * used to configure operation of the availbaility data scraping. 
* [config_price.json](./config/config_price.json)
  * used to configure operation of the availbaility data scraping. Note, the scraper takes a
    list of configurations that all will be run for each ID - this can be used to run multiple
    dates for pricing.
* [constants.py](./config/constants.py)
  * used to configure the s3 locations in which the configs should live
* [id_config.json](./config/id_config.json)
  * contains a list of lists of IDs to be scraped. 
  
The scraper is meant to be run on AWS Batch. Batch provides an easy way to run many parallel 
jobs at once. When running in Batch, the job should be run as an 
["Array Job"](https://docs.aws.amazon.com/batch/latest/userguide/array_jobs.html). Array
jobs provide an environment variable "AWS_BATCH_JOB_ARRAY_INDEX" which can be used to control 
logic in the scraper. This variable decides which list in the list of lists in 
[id_config.json](./config/id_config.json) should be used for that instance. This allows us to run 
an array job of size ```len(id_list)``` - more IDs per container = longer job.

## AWS ECR
ECR is a remote container registry on AWS. You can push your docker containers here to be 
downloaded by any service you want to use the container with. If you don't have a repository 
yet, you can run:
```commandline
aws ecr create-repository \
    --repository-name scraper-1 \
    --image-scanning-configuration scanOnPush=true \
    --region us-east-1 >> ./aws/ecr_repo_rsponse.json
```
Before pushing a container you must build it and authenticate your docker client. To build a 
container use: 
```commandline
docker buildx build --platform=linux/amd64 -t scraper-1 .
```
This is slightly different then some tutorials you will see, this is because I needed to build
for linux to run on AWS, I had issues using the default build command with MacOS with M1. You 
can then authenticate with the following command:
```commandline
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin [AWS User ID].dkr.ecr.us-east-1.amazonaws.com
```
Finally, tag and push to the repo:
```commandline
docker tag scraper-1:latest [AWS User ID].dkr.ecr.us-east-1.amazonaws.com/scraper-1:latest
docker push [AWS User ID].dkr.ecr.us-east-1.amazonaws.com/scraper-1:latest
```

## AWS Batch Setup
* stuff
```commandline
aws batch create-compute-environment --cli-input-json file://aws/batch_compute_envi_config.json
aws batch create-job-queue --cli-input-json file://aws/aws_batch_job_queue.json
aws batch register-job-definition --cli-input-json file://aws/aws_batch_job_def.json
aws batch submit-job --cli-input-json file://aws/submit_batch_job.json
aws batch submit-job --cli-input-json file://aws/submit_batch_job_array.json
```

## EventBridge
* stuff
```commandline
aws events put-rule --name "daily-id-scraper-job" --schedule-expression "cron(0 5 * * ? *)"
aws events put-targets --rule "daily-id-scraper-job" --cli-input-json file://aws/eventbridge_target.json
```
