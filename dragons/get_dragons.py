import json
import boto3
import os
from decimal_reformat import DecimalEncoder


table_name = os.environ.get('DYNAMO_TABLE', 'dragons-table')
region = os.environ.get('REGION_NAME', 'us-east-1')
dynamodb = boto3.resource('dynamodb', region)
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    response = table.scan()
    print(response)
    return {
        "statusCode": 200,
        "body": json.dumps(response['Items'], cls=DecimalEncoder),
    }
