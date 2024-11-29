"""Deprecated functions module"""


from langchain_community.tools import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase

from app.database.postgres_client import SessionFactory
from app.settings import DATABASE_URL
from app.settings import db_table
from typing import Optional
import pandas as pd


# Helper functions for the Agent Tools
def get_stocks_data(ticker):
    # Execute the query directly to get the stock data as a DataFrame
    query = f"""
            SELECT *
            FROM {db_table}
            WHERE ticker = '{ticker}'
        """
    with SessionFactory() as session:
        stocks_df = pd.read_sql_query(query, session.bind)

    return stocks_df


def stock_analysis(ticker: str, analysis_type: Optional[str] = None):
    """Helper functions for the tools"""
    hist = get_stocks_data(ticker)
    if analysis_type == "highest":
        return f"The highest stock price of {ticker} is {hist['High'].max()}"
    elif analysis_type == "average":
        return f"The average stock price of {ticker} is {hist['Close'].mean()}"
    else:
        return "Invalid analysis type. Use 'highest' or 'average'."



# # Define the tool to interact with the database
db = SQLDatabase.from_uri(DATABASE_URL)


def optimized_query(ticker: str, table: str = "stocks_table"):
    query = f"""
        SELECT *
        FROM {table}
        WHERE ticker = '{ticker}'
        LIMIT 5;  # Adjust limit as per performance requirements
    """
    return query


def run_optimized_query_with_error_handling(ticker: str):
    try:
        query = optimized_query(ticker)
        result = db.execute(query)
        return result
    except Exception as e:
        return f"Error running query: {e}"


query_tool = QuerySQLDataBaseTool(db=db, query_func=run_optimized_query_with_error_handling)
