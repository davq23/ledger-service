import datetime
from ulid import ULID
from libs.exceptions import ApplicationException
from models.ledger import Ledger
from models.paypal import PaypalEventInput
from repositories.ledger import register_ledger
from config.config import app_config
from db.db import db_connection


def paypal_event_handler(input: PaypalEventInput):
    resource = input.get_resource()

    if resource != None:
        ledger = resource.as_ledger()
        ledger.reason = input.summary
        ledger.details = input.json()
        register_ledger(db_connection, ledger)
    else:
        raise ApplicationException('Unsupported paypal resource')