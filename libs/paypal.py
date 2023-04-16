from base64 import b64decode, b64encode
from http import client
import json
from ulid import ULID
from models.paypal import PaypalAuthorizationResponse, PaypalEventInput, PaypalWebhookSignature
from repositories.ledger import register_ledger
from config.config import app_config
from db.db import db_connection
from urllib.parse import urlencode

async def paypal_login(client_id: str, client_secret: str):
    http_connection = client.HTTPSConnection(host=app_config['PAYPAL_REST_API_URL'], timeout=app_config['PAYPAL_REST_API_TIMEOUT'])
    token = b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode("ascii")
    headers = {
        'Authorization': f"Basic {token}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = {
        'grant_type': 'client_credentials'
    }
    http_connection.request('POST', '/v1/oauth2/token', headers=headers, body=urlencode(body))

    http_response = http_connection.getresponse()

    bytes = http_response.read()

    response_str = bytes.decode('utf-8')

    paypal_response = json.loads(response_str)

    if paypal_response is None or 'error' in paypal_response:
        return None
    
    return PaypalAuthorizationResponse.from_dict(paypal_response)

async def paypal_verify_webhook_signature(access_token: str, webhook_signature: PaypalWebhookSignature):
    http_connection = client.HTTPSConnection(host=app_config['PAYPAL_REST_API_URL'], timeout=app_config['PAYPAL_REST_API_TIMEOUT'])
    headers = {
        'Authorization': f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }
    body = "{"
    body += f'"transmission_id":"{webhook_signature.transmission_id}","transmission_time":"{webhook_signature.transmission_time}",'
    body += f'"transmission_sig":"{webhook_signature.transmission_sig}",'
    body += f'"cert_url":"{webhook_signature.cert_url}","auth_algo":"{webhook_signature.auth_algo}",'
    body += f'"webhook_id":"{webhook_signature.webhook_id}","webhook_event":{webhook_signature.rawSignature}'
    body += "}"

    http_connection.request(
        'POST',
        '/v1/notifications/verify-webhook-signature',
        headers=headers,
        body=body
    )

    http_response = http_connection.getresponse()

    bytes = http_response.read()

    response_str = bytes.decode('utf-8')
    paypal_response = json.loads(response_str)

    if paypal_response is None or 'verification_status' not in paypal_response:
        return 'FAILURE'

    return paypal_response['verification_status']

async def paypal_handle_event(input: PaypalEventInput, rawBody: str, access_token: str, headers: dict):
    webhook_signature = PaypalWebhookSignature.from_dict(headers)
    webhook_signature.webhook_id = app_config['PAYPAL_WEBHOOK_ID']
    webhook_signature.rawSignature = rawBody
    webhook_signature.webhook_event = input.to_dict()

    status = await paypal_verify_webhook_signature(access_token, webhook_signature)

    if status != 'SUCCESS':
        return
    
    resource = input.get_resource()

    if resource != None:
        ledger = resource.as_ledger()
        ledger.reason = input.summary
        register_ledger(db_connection, ledger)