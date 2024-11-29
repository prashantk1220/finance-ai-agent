from sqlalchemy.orm import Session
from sqlalchemy import func
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Query
from app.database.postgres_client import get_db, StockData


router = APIRouter()


@router.get("/v1/stock/{ticker}/highest-price")
async def get_highest_price(ticker: str, db: Session = Depends(get_db)):
    # Query to get the highest Close price for a given ticker
    highest_price = db.query(func.max(StockData.close_price).label('highest_price')).filter(
        StockData.ticker == ticker).scalar()

    if highest_price is None:
        # If no data found, raise an exception
        raise HTTPException(status_code=404, detail="Ticker not found or no data available")

    return JSONResponse(
        content={"highest_price": float(highest_price)},
        status_code=200
    )


# @router.get("/news/{ticker}")
# async def get_news(ticker: str, topic: str = Query(default="", description="Filter by topic")):
#     collection = news_db[ticker]
#     articles = collection.find({"content": {"$regex": topic, "$options": "i"}})
#     return [{"title": a["title"], "content": a["content"]} for a in articles]