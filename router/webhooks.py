from fastapi import FastAPI, Request

from libs.paypal import paypal_event_handler
from models.paypal import PaypalEventInput

webhooks_app = FastAPI()
paypal_webhook = FastAPI()

@paypal_webhook.post('/notification')
async def paypal_notification(input: PaypalEventInput):
    paypal_event_handler(input)
    return {"status": "OK"}

webhooks_app.mount('/paypal', paypal_webhook)