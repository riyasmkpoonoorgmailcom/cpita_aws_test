import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    record = client.get_item(TableName='customer_details',Key={'telephone_number': {'N' : str(event['telephone_number'])}})
    customer_exists =  not record.get('Item', {}) == {}
    has_phone_password = not  record.get('Item', {}).get('telephone_password', {}) == {}
    result = {}
    result['customer_exists'] = customer_exists
    result['has_phone_password'] = has_phone_password
    print(result)
    # TODO implement
    return json.dumps(result) 