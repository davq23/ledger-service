from pydantic import BaseModel

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
            resource.seller_receivable_breakdown.net_amount.currency_code = self.resource['seller_receivable_breakdown']['net_amount']['currency_code']
            resource.seller_receivable_breakdown.net_amount.value = self.resource['seller_receivable_breakdown']['net_amount']['value']
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

class PaypalCaptureResource:
    disbursement_mode: str
    amount: PaypalAmount
    create_time: str
    update_time: str
    final_capture: bool
    seller_receivable_breakdown: PaypalSellerReceivableBreakdown

    def as_ledger(self):
        ledger = Ledger()
        ledger.amount = f"-{self.amount.value}"
        ledger.currency = self.amount.currency_code
        ledger.added_at = self.create_time.replace('T', ' ').replace('Z', '')
        ledger.user_id = '11111'

        return ledger