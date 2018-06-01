import requests
import json
import csv

def load_keys(filename):

    gbdx_dict = {}
    with open(filename) as tsv:
        for line in csv.reader(tsv, dialect="excel-tab"):
            gbdx_dict[line[0]] = line[1]
    
    
    return gbdx_dict


username = "my_user_name"
password = "my_password"
api_key = "my_api_key"

gbdx_fi = r"C:\Projects\GBDX\user_info.txt"
gbdx_info = load_keys(gbdx_fi)
username = gbdx_info['E-mail']
password = "@kron0hi0rules"
api_key = gbdx_info['APIKey']
url = 'https://geobigdata.io/auth/v1/oauth/token/'
headers = {"Authorization": "Basic " + api_key, "Content-Type": "application/x-www-form-urlencoded"}
params = {"grant_type": "password", "username": username, "password": password }
results = requests.post(url, headers=headers, data=params)

if results.status_code == 200:
    access_token = results.json()['access_token']
    print (access_token)
    print (results.json())
    
