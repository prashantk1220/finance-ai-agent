from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from starlette.responses import RedirectResponse

from app.api.models import QueryResponse, QueryRequest
from app.langchain_agent import LLMAgent, AgentException
from app.api.endpoints import router
from app import settings

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()
app.include_router(router)


# Shared LLM agent instance
llm_agent = None


@app.on_event("startup")
async def startup_event():
    """Initialize the LLM agent on app startup."""
    load_dotenv()
    global llm_agent
    llm_agent = LLMAgent(model=settings.llm_model)
    logger.info("LLM agent successfully initialized on startup.")


@app.on_event("shutdown")
async def shutdown_event():
    """Perform cleanup if necessary."""
    global llm_agent
    llm_agent = None
    logger.info("LLM agent cleaned up on shutdown.")


# Dependency to get the LLM agent
def get_llm_agent() -> LLMAgent:
    if llm_agent is None:
        raise RuntimeError("LLM agent has not been initialized!")
    return llm_agent


@app.post("/v1/query/{ticker}", response_model=QueryResponse)
async def query_agent(request: QueryRequest, ticker: str, agent: LLMAgent = Depends(get_llm_agent)):
    try:
        response = agent.query_stock_agent(request.question, ticker)
        return QueryResponse(agent_message=response)

    except AgentException as e:
        return QueryResponse(
            agent_message="Agent processing failed",
            detail=str(e)
        )

    except HTTPException as e:
        return QueryResponse(
            agent_message="HTTP error occurred",
            detail=e.detail
        )

    except Exception as e:
        return QueryResponse(
            agent_message="An unexpected error occurred",
            detail=str(e)
        )


@app.get("/")
async def main():
    return RedirectResponse(url="/docs")
