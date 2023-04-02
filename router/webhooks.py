from config.config import app_config
from http import client
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from libs.paypal import paypal_handle_event, paypal_login, paypal_verify_webhook_signature
from models.paypal import PaypalEventInput, PaypalWebhookSignature

webhooks_app = FastAPI()
paypal_webhook = FastAPI()

@paypal_webhook.middleware('http')
async def paypal_webhook_check(request: Request, call_next):
    authorization_response = await paypal_login(app_config['PAYPAL_REST_API_CLIENT_ID'], app_config['PAYPAL_REST_API_CLIENT_SECRET'])
    
    if authorization_response is None:
        return JSONResponse({'msg': 'Auth not possible'})
    
    request.state.authorization_response = authorization_response

    return await call_next(request)

@paypal_webhook.post('/notification')
async def paypal_notification(request: Request, input: PaypalEventInput):
    await paypal_handle_event(input, request.state.authorization_response.access_token, request.headers)
    return {"status": "OK"}

webhooks_app.mount('/paypal', paypal_webhook)