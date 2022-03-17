import json
import boto3
import os


dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMO_TABLE', 'dragons-table')
region = os.environ.get('REGION_NAME', 'us-east-1')
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    name = event['pathParameters']['name']
    table.delete_item(
        Key={
            'name': name
        }
    )
    response = {
        'message': 'Item deleted'
    }
    return {
        "statusCode": 200,
        "body": json.dumps(response),
    }
