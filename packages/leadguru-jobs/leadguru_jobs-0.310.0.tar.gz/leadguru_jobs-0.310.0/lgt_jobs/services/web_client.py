import requests
from requests import Response

from ..env import portal_url, service_account_email, service_account_password


class BaseHttpClient:
    api_version: str = None
    token: str = None

    def _create_default_headers(self):
        return {'Authorization': f"Bearer {self.token}"}


class V3ServerClient(BaseHttpClient):
    api_version = 'api/v3'

    def __init__(self):
        self.token = BillingServerClient.login(service_account_email, service_account_password)

    def update_user_lead(self, message_id: str, email: str, slack_channel: str, board_id: str, status: str) -> dict:
        payload = {
            'message_id': message_id,
            'user_email': email
        }

        update_lead_payload = {
            'slack_channel': slack_channel,
            'board_id': board_id,
            'status': status,
        }
        headers = self._create_default_headers()
        return requests.post(f'{portal_url}/{self.api_version}/user_leads/update',
                             headers=headers, params=payload, json=update_lead_payload).json()

    def save_lead_from_contact(self, sender_id: str, email: str, message: str = None) -> Response:
        payload = {
            'sender_id': sender_id,
            'user_email': email,
            'message': message
        }
        headers = self._create_default_headers()
        return requests.post(f'{portal_url}/{self.api_version}/user_leads/save_from_contact',
                             headers=headers, params=payload)


class BillingServerClient:
    api_version = 'api'

    @staticmethod
    def login(email: str, password: str) -> str:
        payload = {
            'email': email,
            'password': password
        }
        response = requests.post(f'{portal_url}/{BillingServerClient.api_version}/login', json=payload).json()
        return response['access_token']
