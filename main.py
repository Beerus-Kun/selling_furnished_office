from typing import Optional
from fastapi import FastAPI
import schemas.account as SCAccount
import uvicorn
import model.connect as Connect
from dotenv import load_dotenv
from routers import account
from routers import product
from routers import bill
load_dotenv()

app = FastAPI()

app.include_router(
    account.router,
    prefix='/account',
    tags=['account']
    )

app.include_router(
    product.router,
    prefix='/product',
    tags=['product']
)

app.include_router(
    bill.router,
    prefix='/bill',
    tags=['bill']
)

@app.get('/')
def index():
    version = Connect.connect()
    return version

@app.post('hello')
def posthello(hel: SCAccount.Hello):
    return f'title: {hel.title}'


if __name__ == "__main__":
    uvicorn.run(app)