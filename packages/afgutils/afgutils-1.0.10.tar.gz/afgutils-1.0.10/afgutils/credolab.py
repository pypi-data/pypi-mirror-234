from os import getenv
from afgutils.db import DB
import requests
from datetime import datetime


class CredoLab:
    GET_TOKEN_QUERY = """
            SELECT * FROM credolab.token ORDER BY id DESC LIMIT 1;
            """

    INSERT_TOKEN_QUERY = """
            INSERT INTO credolab.token (access_token, token_type, issued, expires, refresh_token)
            VALUES (?, ?, ?, ?, ?);
            """

    def __init__(self):
        self.email = getenv('credolab_user_email')
        self.password = getenv('credolab_password')
        self.token = None
        self.rep_conn = DB.get_connection('rep')
        self.service_url = getenv('credolab_base_url')

    def get_token(self):
        if self.token is None:
            self.token = self._get_token()
        return self.token

    def _get_token(self):
        with self.rep_conn.cursor() as cursor:
            token_details = DB.execute(cursor, self.GET_TOKEN_QUERY, fetch='one')

        if token_details is None or token_details['expires'] < datetime.utcnow():
            token = self._fetch_token()
        else:
            token = token_details['access_token']

        return token

    def _fetch_token(self):
        url = f'{self.service_url}/v6.0/account/login'
        payload = {'userEmail': self.email, 'password': self.password}
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise Exception(f'Failed to fetch token from CredoLab: {response.text}')
        token_details = response.json()
        self._save_token(token_details)
        return token_details['access_token']

    def _save_token(self, token: dict) -> None:

        with self.rep_conn.cursor() as cursor:
            DB.execute(cursor, self.INSERT_TOKEN_QUERY,
                       parameters=(token['access_token'], token['token_type'], token['.issued'],
                                   token['.expires'], token['refresh_token']))
        self.rep_conn.commit()
        return token['access_token']

    def _refresh_token(self, bearer_token: str, refresh_token: str) -> str:
        url = f'{self.service_url}/v6.0/account/login/refreshToken'
        payload = {'refreshToken': refresh_token}
        headers = {'Authorization': f'Bearer {bearer_token}'}
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise Exception(f'Failed to refresh token from CredoLab: {response.text}')
        token_details = response.json()
        self._save_token(token_details)
        return token_details['access_token']
