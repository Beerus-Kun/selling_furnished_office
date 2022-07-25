from typing import Optional
from fastapi import FastAPI
import schemas.account as SCAccount
import uvicorn
import model.connect as Connect
from routers import account
from routers import product

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

@app.get('/')
def index():
    version = Connect.connect()
    return version

@app.post('hello')
def posthello(hel: SCAccount.Hello):
    return f'title: {hel.title}'


if __name__ == "__main__":
    uvicorn.run(app)