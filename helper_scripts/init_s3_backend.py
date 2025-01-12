import sys
import boto3
import json

def init_s3_backend(bucket_name: str, key_paths: list, region: str):
    s3 = boto3.client('s3')
    
    # Check if bucket exists
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} already exists")
    except:
        print(f"Creating bucket {bucket_name}...")
        
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
    
    # Iterate over the list of keys
    for key_path in key_paths:
        # Check if key exists
        try:
            s3.head_object(Bucket=bucket_name, Key=key_path)
            print(f"Key already exists: s3://{bucket_name}/{key_path}")
        except:
            print(f"Creating empty key at s3://{bucket_name}/{key_path}")
            s3.put_object(
                Bucket=bucket_name,
                Key=key_path,
                Body=""
            )

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python init_s3_backend.py <bucket-name> <region> <key-path-1> [<key-path-2> ... <key-path-n>]")
        print("Example: python init_s3_backend.py aidoc-devops-cloud-ex-bucket2 eu-west -1 tf/order-processing tf/another-key")
        sys.exit(1)
        
    bucket_name = sys.argv[1]
    region = sys.argv[2]
    key_paths = sys.argv[3:]
    
    init_s3_backend(bucket_name, key_paths, region) 