"""Module to be scheduled as cron job or APScheduler to run periodically to fetch data"""
from datetime import datetime

import yfinance as yf
from sqlalchemy.orm import Session

from app.database.postgres_client import StockData, get_db


def fetch_and_store_stock_data(ticker: str, session: Session):
    """
    Fetches the historical 1 year data for the given ticker
    This can be modified based on requirement
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    hist.reset_index(inplace=True)

    # Convert the dataframe to a list of dictionaries for SQLAlchemy insert
    stock_data_entries = []
    for _, row in hist.iterrows():
        stock_data_entries.append({
            'ticker': ticker,
            'trade_date':  row['Date'].date() if isinstance(row['Date'], datetime) else row['Date'],
            'open_price': row['Open'],
            'high_price': row['High'],
            'low_price': row['Low'],
            'close_price': row['Close'],
            'volume': row['Volume']
        })

    # Bulk insert into the database
    with session.begin():
        session.bulk_insert_mappings(StockData, stock_data_entries)


if __name__ == '__main__':

    # example tickers to be stored
    tickers = ['AAPL', 'MSFT', 'TSLA', 'AMZN']
    with get_db() as session:
        for ticker in tickers:
            fetch_and_store_stock_data(ticker, session)

    # test
    # with get_db() as session:
    #     ticker = 'AAPL'
    #     stock_data = get_stock_data_by_ticker(ticker)
    #     for data in stock_data:
    #         print(
    #             f"Data ID: {data.data_id}, Ticker: {data.ticker}, Date: {data.trade_date},
    #             Open Price: {data.open_price}")
