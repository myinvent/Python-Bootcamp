import json
import boto3
from datetime import datetime

from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb')
table_name = 'pico-weather'

def lambda_handler(event, context):
    http_method = event['httpMethod']
    
    if http_method == 'POST':
        return handle_post_request(event)
    elif http_method == 'GET':
        return handle_get_request()
    
    return {
        'statusCode': 400,
        'body': json.dumps('Invalid request')
    }

def handle_post_request(event):
    try:
        request_body = json.loads(event['body'])
        
        temperature = request_body.get('temperature')
        humidity = request_body.get('humidity')
        light = request_body.get('light')
        
        if temperature is not None and humidity is not None and light is not None:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            table = dynamodb.Table(table_name)
            table.put_item(
                Item={
                    'timestamp': timestamp,
                    'temperature': temperature,
                    'humidity': humidity,
                    'light': light
                }
            )
            
            return {
                'statusCode': 200,
                'body': json.dumps(f'Successfully store data at {timestamp}')
            }
        
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid data format')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }

def handle_get_request():
    try:
        table = dynamodb.Table(table_name)
        response = table.scan()
        sensor_data = response['Items']
        
        return {
            'statusCode': 200,
            'body': json.dumps(sensor_data, cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
