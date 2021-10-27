'''
A file for testing whether External Identities works in a basic sense.
'''

import requests
import jwt
import json
import base64
from datetime import datetime, timedelta
from rich.console import Console

console = Console()

KEY = "REPLACE ME"
KEY_ID = "REPLACE ME"
ANSWERS_ENDPOINT = "https://liveapi.yext.com/v2/accounts/me/answers/vertical/query"
MINT_METHOD = 'SELF' #can be YEXT or SELF

headers = {"kid": KEY_ID}
payload = {
    "aud": ["/v2/accounts/me/answers"],
    "exp": 32525530793,
    "query": {
        "v" : "20200101",
        'local': 'en',
        'version': "STAGING",
        "identity": json.dumps({
            "externalIdentities":
            [
                {
                    "source": "REPLACE ME",
                    "identities": "REPLACE ME"
                }
            ]
        })
    }
}

if MINT_METHOD == 'SELF':
    token = jwt.encode(payload, KEY, headers=headers, algorithm="HS256")
    print(token)
elif MINT_METHOD == 'YEXT':
    token_endpoint = "http://gen-app01.prod.us2.yext.com:9060/consumerauth/create"
    full_body = {**payload, **headers}
    # Named differently for some reason.
    full_body['query_params'] = full_body['query']
    response = requests.post(token_endpoint, json=full_body)
    token = response.json()['token']
    print(token)

head = {'Authorization': f'Bearer {token}'}
params = {
    'input': 'REPLACE WITH QUERY',
    'experienceKey': 'REPLACE ME',
    'verticalKey': 'REPLACE ME'
}
response = requests.get(ANSWERS_ENDPOINT, params=params, headers=head)
console.log(response.json())
console.log(len(response.json()['response']['results']))