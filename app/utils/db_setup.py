import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def create_users_table():
    return dynamodb.create_table(
        TableName='users',
        KeySchema=[{'AttributeName': 'uuid', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'uuid', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )

def create_documents_table():
    return dynamodb.create_table(
        TableName='documents',
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
