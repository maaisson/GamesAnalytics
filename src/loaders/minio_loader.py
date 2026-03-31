import os
import boto3
import json


def get_minio_client():
    return boto3.client(
        "s3",
        endpoint_url=f"http://{os.getenv('MINIO_ENDPOINT')}",
        aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
    )


def upload_json(bucket_name: str, object_name: str, content: bytes):
    client = get_minio_client()
    client.put_object(
        Bucket=bucket_name,
        Key=object_name,
        Body=content,
        ContentType="application/json"
    )


def read_json(bucket_name: str, object_name: str):
    client = get_minio_client()
    
    response = client.get_object(
        Bucket=bucket_name,
        Key=object_name
    )
    
    content = response["Body"].read().decode("utf-8")
    
    return json.loads(content)

def list_objects(bucket_name: str, prefix: str):
    client = get_minio_client()
    response = client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    return [obj["Key"] for obj in response.get("Contents", [])]