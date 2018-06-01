import requests
        
# Get nricklin user token
username = 'joseph.mcglinchy@colorado.edu'
password = '@kron0hi0rules'
api_key = 'LTNVbVJNZUwuZlVzTHFiSGtMRWFsYklfYS5WSXdxTzdfb1VVWnVaaDp4ZzRsR2M2b3pvdVg9Y2lHUi4/SFdaN2pIaUpUNWNPLkEzSU9aRUdvdmVXTE1FV1ZvOFdATnhTUDdoZnAhQkNOWG1YaENWY0NkelB4dUBQZE5rQzpjZm9raG9EdkBOV1BxNlNjNVp4MERyZnNPXzhJU18zTlRfOUtvO1AxRDFqYQ=='

prefix = 'd7dcf387-b4a7-4c83-90ad-f7e26883a331'
s3_path = r's3://gbd-customer-data/{}/'.format(prefix)

token_url = 'https://geobigdata.io/auth/v1/oauth/token/'

headers = {'Authorization': "Basic %s" % api_key}
body = {"grant_type":'password', 'username': username, 'password': password}

r = requests.post(token_url, headers=headers, data=body)

access_token = r.json()['access_token']

url          = 'https://geobigdata.io/s3creds/v1/prefix?duration=36000'
headers      = {'Content-Type': 'application/json',"Authorization": "Bearer " + access_token}
results      = requests.get(url,headers=headers)

# print out the json results
print "[DEFAULT]"
print "aws_secret_access_key=" + results.json()['S3_secret_key']
print "aws_access_key_id=" + results.json()['S3_access_key']
print "aws_session_token=" + results.json()['S3_session_token']



# Dump credentials into your aws cli credentials file:
# python create_s3tmp_creds.py > ~/.aws/credentials
# python create_s3tmp_creds.py > C:/users/jomc9287/.aws/credentials (windows)


# Finally, use the AWS CLI to list items in your storage location:
# aws s3 ls s3://gbd-customer-data/<your_prefix>/