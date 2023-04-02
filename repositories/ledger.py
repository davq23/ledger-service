from datetime import date, datetime
from config.config import app_config
from models.ledger import Ledger
from typing import Union

MAX_LEDGER_FETCH = 1000

def register_ledger(conn, ledger: Ledger):
    cursor = conn.cursor()
    
    cursor.execute(
        f"INSERT INTO {app_config['DB_PREFIX']}ledger (id, reason, amount, charge_id, user_id, details, added_at) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (ledger.id, ledger.reason, ledger.amount, ledger.charge_id, ledger.user_id, ledger.details, ledger.added_at,)
    )

    cursor.close()

    conn.commit()


def get_ledger(conn, id: str):
    ledger: Union[Ledger, None] = None

    cursor = conn.cursor()

    cursor.execute(
        f"SELECT  id, reason, amount, charge_id, added_at, user_id FROM {app_config['DB_PREFIX']}ledger WHERE id = %s",
        (id,)
    )

    row = cursor.fetchone()

    if row != None:
        ledger = Ledger()
        (ledger.id, ledger.reason, ledger.amount, ledger.charge_id, ledger.added_at, ledger.user_id) = row

    cursor.close()

    return ledger

def get_ledgers_by_user_and_dates(conn, user_id: str, start: str, end: str, offset: str = ""):
    ledgers: list[Ledger] = []

    cursor = conn.cursor()

    if offset == "":
        offset = start

    cursor.execute(
        f"SELECT  id, reason, amount, charge_id, added_at, user_id FROM {app_config['DB_PREFIX']}ledger WHERE"+
        ' user_id = %s AND added_at >= %s AND added_at <= %s AND added_at >= %s ORDER BY added_at DESC',
        (user_id, start, end, offset,)
    )

    all_rows = cursor.fetchmany(size=MAX_LEDGER_FETCH)

    for row in all_rows:
        ledger = Ledger()
        (ledger.id, ledger.reason, ledger.amount, ledger.charge_id, ledger.added_at, ledger.user_id) = row
        ledgers.append(ledger)

    return ledgers