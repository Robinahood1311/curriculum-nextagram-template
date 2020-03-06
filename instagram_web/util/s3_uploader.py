import boto3
import botocore
from config import Config

s3 simple storage service
s3 = boto3.client(
    "s3",
    aws_access_key
)
