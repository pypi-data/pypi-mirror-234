from os import getenv
from datetime import datetime, timezone
import hashlib
import json
import requests


def generate_token() -> str:
    access_key = getenv("advanceai_access_key")
    secret_key = getenv("advanceai_secret_key")
    utc_now = datetime.now(timezone.utc)
    time_epoch_now = int(utc_now.timestamp()*1000)
    signature = hashlib.sha256(f"{access_key}{secret_key}{time_epoch_now}".encode()).hexdigest()

    token_url = "https://sg-api.advance.ai/openapi/auth/ticket/v1/generate-token"
    token_body = json.dumps({'accessKey': access_key,
                             'signature': signature,
                             'timestamp': time_epoch_now})
    token_headers = {'Content-Type': 'application/json'}
    token_response = requests.post(token_url, headers=token_headers, data=token_body)
    return token_response.json()['data']['token']