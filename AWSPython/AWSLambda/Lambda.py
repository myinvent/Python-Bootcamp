import json  # Importing the JSON module for data serialization and deserialization
import boto3  # Importing the Boto3 library for interacting with AWS services
from datetime import datetime  # Importing the datetime module to work with timestamps
from decimal import Decimal  # Importing the Decimal class for decimal number handling

# Creating a custom JSONEncoder class to handle Decimal objects
class DecimalEncoder(json.JSONEncoder): 
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

# Creating a DynamoDB resource object using Boto3
dynamodb = boto3.resource("dynamodb")

# Setting the name of the DynamoDB table
table_name = "pico-weather-db"

# AWS Lambda function handler
def lambda_handler(event, context):  
    # Retrieving the HTTP method from the event
    http_method = event["httpMethod"]
    
    # Handling a POST request
    if http_method == "POST":  
        # Calling the function to handle the POST request
        return handle_post_request(event)
    
    # Handling a GET request
    elif http_method == "GET":  
        # Calling the function to handle the GET request
        return handle_get_request()

    # Returning an invalid request response as JSON
    return {
        "statusCode": 400,
        "body": json.dumps("Invalid request")
    }

# Function to handle POST requests
def handle_post_request(event):  
    try:
        # Parsing the request body from the event
        request_body = json.loads(event["body"])

        # Extracting temperature, humidity and light data from the request body
        temperature = request_body.get("temperature")
        humidity = request_body.get("humidity")
        light = request_body.get("light")
        
        # Checking if all values are present
        if temperature is not None and humidity is not None and light is not None:
            
            # Generating a timestamp string
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Accessing the DynamoDB table
            table = dynamodb.Table(table_name)

            # Storing the item in the table
            table.put_item(
                Item={
                    "timestamp": timestamp,
                    "temperature": temperature,
                    "humidity": humidity,
                    "light": light
                }
            )

            # Returning a success response as JSON
            return {
                "statusCode": 200,
                "body": json.dumps(f"Successfully store data at {timestamp}")
            }

        # Returning an invalid data format response as JSON
        return {
            "statusCode": 400,
            "body": json.dumps("Invalid data format")
        }
    
    # Handling exceptions
    except Exception as e:
        # Returning a server error response along with the error message as JSON
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }

# Function to handle GET requests
def handle_get_request():  
    try:
        # Accessing the DynamoDB table
        table = dynamodb.Table(table_name)

        # Scanning the table to retrieve all items
        response = table.scan()

        # Extracting the sensor data from the response
        sensor_data = response["Items"]

        # Returning the sensor data as JSON
        return {
            "statusCode": 200,
            "body": json.dumps(sensor_data, cls=DecimalEncoder)
        }
        
    # Handling exceptions
    except Exception as e:
        # Returning a server error response along with the error message
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }