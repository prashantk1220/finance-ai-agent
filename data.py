import yfinance as yf
from pymongo import MongoClient
import psycopg2
from sqlalchemy import create_engine
import pandas as pd

# PostgreSQL connection
POSTGRES_URI = "postgresql://username:password@localhost:5432/finance_db"
pg_engine = create_engine(POSTGRES_URI)

# MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")
news_db = mongo_client['finance_news']


def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    hist.reset_index(inplace=True)
    hist.to_sql(ticker, pg_engine, if_exists='replace', index=False)
    return hist


def fetch_news_data(ticker):
    # Placeholder for fetching news. RSS feeds or web scraping can be used.
    articles = [{"ticker": ticker, "title": "Sample Article", "content": "Content goes here"}]
    news_collection = news_db[ticker]
    news_collection.insert_many(articles)
    return articles
