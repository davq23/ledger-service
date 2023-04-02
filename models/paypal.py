import json
from pydantic import BaseModel
from ulid import ULID

from models.ledger import Ledger

PAYPAL_EVENT_TYPE_PAYMENT_SALE_COMPLETED = 'PAYMENT.SALE.COMPLETED'
PAYPAL_EVENT_TYPE_PAYMENT_CAPTURE_COMPLETED = 'PAYMENT.CAPTURE.COMPLETED'

class PaypalEventInput(BaseModel):
    id: str
    create_time: str
    resource_type: str
    event_type: str
    summary: str
    resource: dict

    def get_resource(self):
        resource = None

        if self.event_type == PAYPAL_EVENT_TYPE_PAYMENT_CAPTURE_COMPLETED:
            resource = PaypalCaptureResource()
            resource.amount = PaypalAmount()
            resource.amount.currency_code = self.resource['amount']['currency_code']
            resource.amount.value = self.resource['amount']['value']
            resource.disbursement_mode = self.resource['disbursement_mode']
            resource.create_time = self.resource['create_time']
            resource.update_time = self.resource['update_time']
            resource.final_capture = self.resource['final_capture']
            resource.seller_receivable_breakdown = PaypalSellerReceivableBreakdown()
            resource.seller_receivable_breakdown.gross_amount = PaypalAmount()
            resource.seller_receivable_breakdown.gross_amount.currency_code = self.resource['seller_receivable_breakdown']['gross_amount']['currency_code']
            resource.seller_receivable_breakdown.gross_amount.value = self.resource['seller_receivable_breakdown']['gross_amount']['value']
            resource.seller_receivable_breakdown.net_amount = PaypalAmount()
            resource.seller_receivable_breakdown.net_amount.currency_code = self.resource['seller_receivable_breakdown']['net_amount']['currency_code']
            resource.seller_receivable_breakdown.net_amount.value = self.resource['seller_receivable_breakdown']['net_amount']['value']
            resource.seller_receivable_breakdown.paypal_fee = PaypalAmount()
            resource.seller_receivable_breakdown.paypal_fee.currency_code = self.resource['seller_receivable_breakdown']['paypal_fee']['currency_code']
            resource.seller_receivable_breakdown.paypal_fee.value = self.resource['seller_receivable_breakdown']['paypal_fee']['value']

        return resource


class PaypalAmount:
    currency_code: str
    value: str

class PaypalSellerReceivableBreakdown:
    gross_amount: PaypalAmount
    paypal_fee: PaypalAmount
    net_amount: PaypalAmount

    def as_dict(self):
        return {
            "gross_amount": {
                "value": self.gross_amount.value,
                "currency_code": self.gross_amount.currency_code
            },
            "net_amount": {
                "value": self.net_amount.value,
                "currency_code": self.net_amount.currency_code
            },
            "paypal_fee": {
                "value": self.paypal_fee.value,
                "currency_code": self.paypal_fee.currency_code
            },
        }

class PaypalCaptureResource:
    disbursement_mode: str
    amount: PaypalAmount
    create_time: str
    update_time: str
    final_capture: bool
    seller_receivable_breakdown: PaypalSellerReceivableBreakdown

    def as_ledger(self):
        ledger = Ledger()
        ledger.id = str(ULID())
        ledger.amount = self.amount.value
        ledger.currency = self.amount.currency_code
        ledger.added_at = self.create_time.replace('T', ' ').replace('Z', '')
        ledger.user_id = '11111'
        ledger.details = json.dumps(self.seller_receivable_breakdown.as_dict())
        return ledger

class PaypalAuthorizationResponse:
    scope: str
    access_token: str
    token_type: str
    app_id: str
    expires_in: int
    nonce: str

    @staticmethod
    def from_dict(dictionary: dict):
        paypal_authorization_response = PaypalAuthorizationResponse()
        paypal_authorization_response.scope = dictionary['scope']
        paypal_authorization_response.access_token = dictionary['access_token']
        paypal_authorization_response.token_type = dictionary['token_type']
        paypal_authorization_response.app_id = dictionary['app_id']
        paypal_authorization_response.expires_in = dictionary['expires_in']
        paypal_authorization_response.nonce = dictionary['nonce']

        return paypal_authorization_response
    
class PaypalWebhookSignature:
    auth_algo: str
    cert_url: str
    transmission_id: str
    transmission_sig: str
    transmission_time: str
    webhook_event: PaypalEventInput
    webhook_id: str

    @staticmethod
    def from_dict(dictionary: dict):
        print(dictionary)
        paypal_webhook_signature = PaypalWebhookSignature()
        paypal_webhook_signature.auth_algo = dictionary['paypal-auth-algo']
        paypal_webhook_signature.cert_url = dictionary['paypal-cert-url']
        paypal_webhook_signature.transmission_id = dictionary['paypal-transmission-id']
        paypal_webhook_signature.transmission_sig = dictionary['paypal-transmission-sig']
        paypal_webhook_signature.transmission_time = dictionary['paypal-transmission-time']

        return paypal_webhook_signature