from decimal import Decimal

import pytest
from app.database.postgres_client import StockData
from app.job_worker import fetch_and_store_stock_data
from datetime import datetime


@pytest.mark.parametrize("ticker", ["AAPL"])
def test_fetch_and_store_stock_data(test_session, ticker):
    """
    Test the fetch_and_store_stock_data function by verifying data is stored
    correctly in the database.
    """
    # Fetch and store stock data
    fetch_and_store_stock_data(ticker, test_session)

    # Query the mock database
    stored_data = test_session.query(StockData).filter_by(ticker=ticker).all()

    # Assert that data was inserted, or output the error message
    assert len(stored_data) > 0, "No stock data was inserted into the database"

    # Validate the stored data
    for data in stored_data:
        assert data.ticker == ticker
        assert isinstance(data.open_price, Decimal)
        assert isinstance(data.high_price, Decimal)
        assert isinstance(data.low_price, Decimal)
        assert isinstance(data.close_price, Decimal)
        assert isinstance(data.volume, (int, float))
