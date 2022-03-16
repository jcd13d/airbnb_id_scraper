import boto3
import json

s3 = boto3.resource('s3',
                    aws_access_key_id= "AKIAQPMOAGEZIPAZQMD3",
                    aws_secret_access_key="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"
                    )

# content_object = s3.Object('jd-s3-test-bucket9', 'config_occ.json')
# file_content = content_object.get()['Body'].read().decode('utf-8')
# json_content = json.loads(file_content)
# print(json_content['Details'])

s3_obj = boto3.client('s3')

s3_clientobj = s3_obj.get_object(Bucket='jd-s3-test-bucket9', Key='test_configs/config_occ.json')
s3_clientdata = s3_clientobj['Body'].read().decode('utf-8')
s3clientlist = json.loads(s3_clientdata)
print(s3clientlist)