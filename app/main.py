
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from app.langchain_agent import query_stock_agent
from app.api.endpoints import router

app = FastAPI()
app.include_router(router)


class QueryRequest(BaseModel):
    question: str


@app.post("/v1/query/{ticker}")
async def query_agent(request: QueryRequest, ticker: str):
    try:
        response = query_stock_agent(request.question, ticker)
        return {"ai-agent": response}
    except Exception as e:
        return {"agent-error": e.message}



@app.get("/")
async def main():
    return RedirectResponse(url="/docs")
