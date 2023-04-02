from datetime import date, datetime
from typing import Union
from models.ledger import Ledger


def register_ledger(conn, ledger: Ledger):
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO ledger (id, reason, amount, charge_id, user_id, added_at) VALUES (%s, %s, %s, %s, %s, %s)',
        (ledger.id, ledger.reason, ledger.amount, ledger.charge_id, ledger.user_id, ledger.added_at,)
    )

    cursor.close()

    conn.commit()


def get_ledger(conn, id: str):
    ledger: Union[Ledger, None] = None

    cursor = conn.cursor()

    cursor.execute(
        'SELECT  id, reason, amount, charge_id, added_at, user_id FROM ledger WHERE id = %s',
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
        'SELECT  id, reason, amount, charge_id, added_at, user_id FROM ledger WHERE'+
        ' user_id = %s AND added_at >= %s AND added_at <= %s AND added_at >= %s ORDER BY added_at DESC',
        (user_id, start, end, offset,)
    )

    all_rows = cursor.fetchmany(size=10000)

    for row in all_rows:
        ledger = Ledger()
        (ledger.id, ledger.reason, ledger.amount, ledger.charge_id, ledger.added_at, ledger.user_id) = row
        ledgers.append(ledger)

    return ledgers