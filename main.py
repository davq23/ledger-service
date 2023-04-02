from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from libs.exceptions import ApplicationException
from router.webhooks import webhooks_app
from router.ledger import ledger_app

app = FastAPI()

@app.middleware('http')
async def standard_response(request: Request, call_next):
    try:
        response = await call_next(request)

        if (isinstance(response, str)):
            return JSONResponse({'msg': response})
    except ApplicationException as app_exception:
        return JSONResponse({'msg': app_exception.__str__()}, 200)
   
    return response

app.mount('/ledger', ledger_app)
app.mount('/webhook', webhooks_app)