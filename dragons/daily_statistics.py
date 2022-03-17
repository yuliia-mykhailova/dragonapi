import json
import boto3
import os
import pandas as pd
from boto3.dynamodb.conditions import Key
from datetime import date


dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMO_TABLE', 'dragons-table')
region = os.environ.get('REGION_NAME', 'us-east-1')
queue_url = os.environ.get('QUEUE_URL')
s3_bucket = os.environ.get('S3_URL')
table = dynamodb.Table(table_name)
client = boto3.client('sqs')
s3_resource = boto3.resource('s3')


def lambda_handler(event, context):
    scan_kwargs = {
        'FilterExpression': Key('created_at').eq(str(date.today()))
    }
    try:
        response = table.scan(**scan_kwargs)
        df = pd.DataFrame(response['Items'])
        df.to_csv('/tmp/stats_from_%s.csv' % date.today(), index=False, header=True)

        s3_resource.Bucket(s3_bucket).upload_file('/tmp/stats_from_%s.csv' % date.today(), 'stats_from_%s.csv' % date.today())
    except Exception as e:
        print(e)
    return {
        "statusCode": 200,
        "body": json.dumps({'message': 'Recorded'}),
    }
