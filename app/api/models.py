from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    agent_message: str
    detail: str = ""
