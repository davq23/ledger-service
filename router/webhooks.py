from config.config import app_config
from db.redis import redis_client
from http import client
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from libs.paypal import paypal_handle_event, paypal_login, paypal_verify_webhook_signature
from models.paypal import PaypalAuthorizationResponse, PaypalEventInput, PaypalWebhookSignature
from repositories.paypal import get_paypal_auth_token, set_paypal_auth_token

webhooks_app = FastAPI()
paypal_webhook = FastAPI()

@paypal_webhook.middleware('http')
async def paypal_webhook_auth_check(request: Request, call_next):
    access_token = get_paypal_auth_token(redis_client)

    authorization_response = None

    if access_token is not None:
        # Access token is valid
        print('ACCESS TOKEN EXISTS')
        authorization_response = PaypalAuthorizationResponse()
        authorization_response.access_token = access_token
    else:
        # Access token expired
        print('ACCESS IS EXPIRED')
        authorization_response = await paypal_login(app_config['PAYPAL_REST_API_CLIENT_ID'], app_config['PAYPAL_REST_API_CLIENT_SECRET'])
        
        if authorization_response is None:
            return JSONResponse({'msg': 'Auth not possible'})
        
        set_paypal_auth_token(
            redis_client,
            authorization_response.access_token,
            authorization_response.expires_in
        )
        
    request.state.authorization_response = authorization_response

    return await call_next(request)

@paypal_webhook.post('/notification')
async def paypal_notification(request: Request, input: PaypalEventInput):
    await paypal_handle_event(input, request.state.authorization_response.access_token, request.headers)
    return {"status": "OK"}

webhooks_app.mount('/paypal', paypal_webhook)