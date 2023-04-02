import os
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import jwt
from db.db import db_connection
from config.config import app_config
from models.ledger import Ledger, LedgerInput
from repositories.ledger import get_ledger, register_ledger

ledger_app = FastAPI()
ledger_app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def no_null_keys(dictionary: dict):
    return dict(filter(lambda pair: (pair[1] != None), dictionary.items()))


@ledger_app.middleware('http')
async def authorization(request: Request, call_next):
    bearerPair = request.headers.get('Authorization')

    if bearerPair is None:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'msg': 'Forbidden'})
    
    bearerPairSplit = bearerPair.split(' ', 2)

    print(bearerPairSplit)

    if (len(bearerPairSplit) != 2):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'msg': 'Forbidden'})
    
    [prefix, bearer] = bearerPair.split(' ', 2)

    if prefix != 'Bearer':
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'msg': 'Forbidden'})

    try:
        payload = jwt.decode(bearer, app_config['SECRET_KEY'], ['HS256'])
    except:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'msg': 'Forbidden'})

    response = await call_next(request)

    return response


@ledger_app.post('/')
async def post(body: LedgerInput):
    ledger = Ledger.createFromInput(body)

    register_ledger(db_connection, ledger)
    
    return no_null_keys(vars(ledger))

@ledger_app.get('/{id}')
async def get(id: str):
    ledger = get_ledger(db_connection, id)

    if ledger is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'msg': 'Not found'})

    return no_null_keys(vars(ledger))