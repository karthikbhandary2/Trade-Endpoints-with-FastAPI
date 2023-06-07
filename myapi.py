from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import datetime as dt

class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")

    price: float = Field(description="The price of the Trade.")

    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")

    counterparty: Optional[str] = Field(default=None, description="The counterparty the trade was executed with. May not always be available")

    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")

    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")

    trade_date_time: dt.datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")

    trade_details: TradeDetails = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")

    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")

    trader: str = Field(description="The name of the Trader")
      


TRADE_1 = Trade(
    assetClass="foo",
    counterparty="guh",
    instrumentId="TSLA",
    instrumentName="Piano",
    tradeDateTime="2023-06-05 10:22",
    tradeDetails=TradeDetails(buySellIndicator='BUY',price=100.0, quantity=10),
    tradeId="1",
    trader="john",
)
TRADE_2 = Trade(
    assetClass="bar",
    counterparty="buz",
    instrumentId="AAPL",
    instrumentName="Guitar",
    tradeDateTime="2023-06-04 11:22",
    tradeDetails=TradeDetails(buySellIndicator='BUY',price=200.0, quantity=1),
    tradeId="2",
    trader="alice",
)
TRADE_3 = Trade(
    assetClass="baz",
    counterparty="nun",
    instrumentId="AMZN",
    instrumentName="Guitar",
    tradeDateTime="2023-06-06 12:22",
    tradeDetails=TradeDetails(buySellIndicator='BUY',price=3.14, quantity=5),
    tradeId="3",
    trader="dan",
)

MOCK_TRADE_DATABASE = {
    "1": TRADE_1,
    "2": TRADE_2,
    "3": TRADE_3,
}

app = FastAPI(title="Trades")

@app.get("/")
def index():
    return {"name": "API Developer Assessment"}

@app.get("/trades/{trade_id}")
def get_trade_by_id(trade_id: str) -> Trade:
    if trade_id not in MOCK_TRADE_DATABASE:
        raise HTTPException(status_code=404)
    return MOCK_TRADE_DATABASE[trade_id]


@app.get("/trade/")
def get_trade_list(search: Optional[str] = None) -> list[Trade]:
    if search is None:
        return list(MOCK_TRADE_DATABASE.values())
    # Search only for matching `trader` values:
    if "trader" in search:
        search = search.split("=")[1]
        return [
            trade for trade in MOCK_TRADE_DATABASE.values()
            if search in trade.trader
        ]
    if "instrumentid" in search:
        search = search.split("=")[1]
        return [
            trade for trade in MOCK_TRADE_DATABASE.values()
            if search in trade.instrument_id
        ]
    if "instrumentname" in search:
        search = search.split("=")[1]
        return[
            trade for trade in MOCK_TRADE_DATABASE.values()
            if search in trade.instrument_name
        ]
    if "assetclass" in search:
        search = search.split("=")[1]
        return [
            trade for trade in MOCK_TRADE_DATABASE.values()
            if search in trade.asset_class
        ]

@app.get("/trade/counterparty")
def get_trade_by_counterparty(party:str) -> list[Trade]:
    return [
        trade for trade in MOCK_TRADE_DATABASE.values()
        if party in trade.counterparty
    ]
@app.get("/trade/byprice")
def get_trade_by_price(minprice: float, maxprice: float) -> list[Trade]:
        if minprice == None and maxprice == None:
            return list(MOCK_TRADE_DATABASE.values())
        return [trade for trade in MOCK_TRADE_DATABASE.values()
                if minprice <= trade.trade_details.price <= maxprice        
        ]

@app.get("/trade/bydate")
def get_trade_by_date(start: dt.datetime, end: dt.datetime) -> list[Trade]:
    if start == None and end == None:
            return list(MOCK_TRADE_DATABASE.values())
    return [
        trade for trade in MOCK_TRADE_DATABASE.values()
        if start <= trade.trade_date_time <= end
    ]
    