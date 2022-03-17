import json
import boto3
import os
from dragon import Dragon
from pydantic import ValidationError


dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMO_TABLE', 'dragons-table')
region = os.environ.get('REGION_NAME', 'us-east-1')
queue_url = os.environ.get('QUEUE_URL')
table = dynamodb.Table(table_name)
client = boto3.client('sqs')


def send_message(name):
    client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps({'name': name})
    )


def lambda_handler(event, context):
    body = json.loads(event.get('body'))
    try:
        dragon_validate = Dragon(
            name=body.get('name'),
            breed=body.get('breed'),
            danger_rating=body.get('danger_rating'),
            description=body.get('description')
        )
    except ValidationError:
        return {
            "statusCode": 400,
            "body": json.dumps({'message': 'Wrong data format'}),
        }
    response = table.put_item(Item=dragon_validate.dict())
    response_body = response.get('ResponseMetadata')
    if response_body.get('HTTPStatusCode') == 200:
        send_message(dragon_validate.name)
    return {
        "statusCode": 201,
        "body": json.dumps({'message': 'Item added'})
    }
