import boto3
import json


client = boto3.client('batch')


def handler(event, context):
    s3 = boto3.resource('s3')

    content_object = s3.Object('airbnb-scraper-bucket-0-0-1', 'running_configs/batch_array_job_sub.json')
    file_content = content_object.get()['Body'].read().decode('utf-8')
    config = json.loads(file_content)

    response = client.submit_job(**config)

    return response
