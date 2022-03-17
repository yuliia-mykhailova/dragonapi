import http.client
import json
import boto3
import os
from botocore.exceptions import ClientError


RECEIVER = 'yuliia.mykhailova.work@gmail.com'
SENDER = 'yuliia.mykhailova.work@gmail.com'

SRI_HOST = 'new_dragon_notify_bot'
TELEGRAM_API_HOST = 'api.telegram.org'
telegram_token = os.getenv('TELEGRAM_TOKEN')
user_id = os.getenv('USER_ID')
TELEGRAM_URL = "https://api.telegram.org/bot{}/sendMessage".format(telegram_token)

queue_url = os.environ.get('QUEUE_URL')
client = boto3.client('sqs')


def handle_send_telegram(name):
    try:
        conn = http.client.HTTPSConnection(TELEGRAM_API_HOST)
        endpoint = f"/bot{telegram_token}/sendDragon"
        payload = {
            'chat_id': user_id,
            'caption': 'New dragon %s added' % name,
        }
        headers = {'content-type': "application/json"}
        conn.request("POST", endpoint, json.dumps(payload), headers)
        res = conn.getresponse()
        return {
            'statusCode': res.status,
            'body': json.dumps('Lambda executed.')
        }
    except Exception as e:
        print('Connection error')
        return {
            'statusCode': 400,
            'body': json.dumps('Error occurred %s' % e)
        }


def handle_send_email(name):
    try:
        client_ses = boto3.client('ses')
        response = client_ses.send_email(
            Destination={
                'ToAddresses': [
                    RECEIVER,
                ],
            },
            Source=SENDER,
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': 'The dragon %s was added' % name,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': 'New dragon notification'
                },
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print('Email sent! Message ID: %s' % response['MessageId'])


def lambda_handler(event, context):
    message_info = event.get('Records')
    receipt_handle = message_info[0]['receiptHandle']

    client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    message_str = message_info[0]['body']
    message_json = json.loads(message_str)
    print('New dragon %s is created' % message_json['name'])
    # handle_send_email(message_json['name'])
    handle_send_telegram(message_json['name'])

    return {
        "statusCode": 200,
        "body": json.dumps({'message': 'Added new dragon: %s' % message_json['name']})
    }
