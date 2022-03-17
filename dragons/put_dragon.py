import json
import boto3
import os
from decimal_reformat import DecimalEncoder
from dragon import Dragon
from pydantic import ValidationError

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMO_TABLE', 'dragons-table')
region = os.environ.get('REGION_NAME', 'us-east-1')
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    name = event['pathParameters']['name']
    body = json.loads(event.get('body'))
    try:
        dragon_validate = Dragon(
            name=name,
            breed=body['breed'],
            danger_rating=body['danger_rating'],
            description=body['description']
        )
    except ValidationError:
        return {
            "statusCode": 400,
            "body": json.dumps({'message': 'Wrong data format'}),
        }
    response = table.update_item(
        Key={
            'name': name
        },
        UpdateExpression="set breed=:b, danger_rating=:d, description=:s",
        ExpressionAttributeValues={
            ':b': body['breed'],
            ':d': body['danger_rating'],
            ':s': body['description']
        },
        ReturnValues="UPDATED_NEW"
    )
    return {
        "statusCode": 201,
        "body": json.dumps(response['Attributes'], cls=DecimalEncoder),
    }
