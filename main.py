from fastapi import FastAPI, Query
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.get("/stock/{ticker}/highest-price")
async def get_highest_price(ticker: str):
    query = f"SELECT MAX(Close) AS highest_price FROM {ticker}"
    result = pd.read_sql(query, pg_engine)
    return {"highest_price": result.to_dict(orient="records")}

@app.get("/news/{ticker}")
async def get_news(ticker: str, topic: str = Query(default="", description="Filter by topic")):
    collection = news_db[ticker]
    articles = collection.find({"content": {"$regex": topic, "$options": "i"}})
    return [{"title": a["title"], "content": a["content"]} for a in articles]

@app.post("/query")
async def query_agent(request: QueryRequest):
    response = agent.run(request.question)
    return {"response": response}
