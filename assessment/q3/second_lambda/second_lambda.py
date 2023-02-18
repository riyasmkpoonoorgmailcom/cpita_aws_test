import json
import boto3
import time

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    record = client.get_item(TableName='customer_details',Key={'telephone_number': {'N' : str(event['telephone_number'])}})
    customer_exists =  not record.get('Item', {}) == {}
    telephone_number = record.get('Item', {}).get('telephone_number', '').get('N', '')
    telephone_password = str(event['telephone_password'])
    f = open("/tmp/myfile.txt", "w")
    f.write("Hello There Hi\n")
    f = open("/tmp/myfile.txt", "r")
    print(f.readline())
    clients3 = boto3.client("s3")
    clients3.upload_file("/tmp/myfile.txt", "captia-test-s3-bucket", "myfile.txt")
    response = clients3.head_object(Bucket='captia-test-s3-bucket', Key='myfile.txt')
    file_size = response['ContentLength']
    file_name = 'myfile.txt'
    file_time_stamp = int(time.time())
    if customer_exists:
        table = boto3.resource('dynamodb').Table('customer_details')
        response = table.update_item(
            Key={'telephone_number': int(telephone_number)},
            UpdateExpression="set telephone_password = :r,file_size = :fs, file_name = :fn, file_time_stamp = :ft",
            ExpressionAttributeValues={
                ':r': int(telephone_password),
                ':fs': file_size,
                ':fn': file_name,
                ':ft': file_time_stamp
            },
            ReturnValues="UPDATED_NEW"
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
