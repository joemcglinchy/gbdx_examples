from gbdxtools import Interface 
from boto import s3

gbdx = Interface() 

#Extract values from customer S3 information
sinfo = gbdx.s3.info
region = 'us-east-1'
access_key = sinfo['S3_access_key']
secret_key = sinfo['S3_secret_key']
session_token = sinfo['S3_session_token']
gbdx_bucket = sinfo['bucket']
headers = {'x-amz-security-token': session_token}
gbdx_prefix = sinfo['prefix']

#Connect to s3 with credentials
conn = s3.connect_to_region(region_name=region,
                            aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key,
                            security_token=session_token)

#Get gbd-customer-data bucket
bucket = conn.get_bucket(bucket_name=gbdx_bucket,
                         headers = headers,
                         validate=False)

#This example will print the entire contents 
#of the customer's prefix, modify as needed.
#See http://docs.aws.amazon.com/AmazonS3/latest/dev/ListingKeysHierarchy.html
#get_all_keys() method could also be used similarly

keys = bucket.list(prefix=gbdx_prefix)

for key in keys:

	print(str(key.name))