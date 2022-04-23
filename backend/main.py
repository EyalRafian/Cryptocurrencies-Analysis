import requests
import yfinance as yf
import simplejson as json
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from models import CoinItem

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class CoinRequest(BaseModel):
    ticker: str


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def fetch_coin_data(id: int):
    """
    Import data from yfinance API
    """
    db = SessionLocal()
    coin = db.query(CoinItem).filter(CoinItem.id == id).first()

    yahoo_data = yf.Ticker(coin.ticker)

    coin.ma200 = yahoo_data.info['twoHundredDayAverage']
    coin.ma50 = yahoo_data.info['fiftyDayAverage']
    coin.price = yahoo_data.info['previousClose']
    coin.shortname = yahoo_data.info['shortName']

    db.add(coin)
    db.commit()


@app.get("/")
def get_coins_table(request: Request, db: Session = Depends(get_db)):
    """
    Reads the coins table from the sqlite database.
    """
    coins = db.query(CoinItem)
    coin_table = {
        "Ticker": [item.ticker for item in coins],
        "Name": [item.shortname for item in coins],
        "Price": [item.price for item in coins],
        "50 Days MA": [item.ma50 for item in coins],
        "200 Days MA": [item.ma200 for item in coins]
    }

    # db.close()
    return JSONResponse(content=json.dumps({"coins": coin_table}))

# async def create_coin(background_tasks: BackgroundTasks):
@app.post("/add")
def create_coin(input: CoinRequest, db: Session = Depends(get_db)):
    """
    Create a new coin and save in the database.
    """
    coin = CoinItem()
    coin.ticker = input.ticker

    db.add(coin)
    db.commit()

    fetch_coin_data(coin.id)

    return {
        "code": "success",
        "message": "coin created"
    }


@app.post("/delete")
async def delete_coin(input: CoinRequest, db: Session = Depends(get_db)):
    """
    Delete an item from the coin database.
    """

    delete_item = db.query(CoinItem).filter(
        CoinItem.ticker == input.ticker).first()

    db.delete(delete_item)
    db.commit()

    return {
        "code": "success",
        "message": "coin deleted"
    }


@app.post("/update")
def update_table(input: CoinRequest, db: Session = Depends(get_db)):
    """
    Replace existing coins data with the latest data from yfinance
    """

    engine.execute('DELETE FROM Coins')  # delete all data from table
    for tick in eval(input.ticker):
        coin = CoinItem()
        coin.ticker = tick

        db.add(coin)
        db.commit()

        fetch_coin_data(coin.id)

    return {
        "code": "success",
        "message": "coin table updated"
    }

