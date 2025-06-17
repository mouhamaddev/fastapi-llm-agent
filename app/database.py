import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table("users")
documents_table = dynamodb.Table("documents")
