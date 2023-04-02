import datetime
from typing import Union

from pydantic import BaseModel
from ulid import ULID

class LedgerInput(BaseModel):
    id: Union[str, None] = None
    reason: str
    amount: float
    charge_id: Union[str, None] = None
    user_id: str
    
class Ledger(object):
    id: str
    reason: str
    amount: float
    user_id: str
    charge_id: Union[str, None] = None
    added_at: Union[str, None] = None
    modified_at: Union[str, None] = None
    deleted_at: Union[str, None] = None
    details: Union[str, None] = None
    currency: str = 'USD'

    @staticmethod
    def createFromInput(input: LedgerInput):
        ledger = Ledger()
        today = datetime.datetime.now()

        if input.id is None:
            ledger.id = str(ULID())
            ledger.added_at = today
        else:
            ledger.id = input.id
            ledger.modified_at = today

        ledger.user_id = input.user_id
        ledger.charge_id = input.charge_id
        ledger.reason = input.reason
        ledger.amount = input.amount

        return ledger