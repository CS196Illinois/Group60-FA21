# HTTP basic authentication in Python

import requests
from requests.auth import HTTPBasicAuth
response = requests.get('http://api.github.com/user', auth=HTTPBasicAuth('username', 'password'))
print('Response Code ' + str(response.status_code))
if response.status_code == 200:
    print('Login successful: '+response.text)
