"""Module to Setup the agent and the tools"""

from langchain.agents import Tool, initialize_agent
from langchain_groq import ChatGroq
from app.utility import get_stocks_data, stock_analysis
from dotenv import load_dotenv

import warnings
warnings.filterwarnings("ignore")

load_dotenv()


_llm_agent = None  # Global variable to store the singleton instance


class AgentException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def setup_agent(model="llama3-8b-8192"):
    """
    Setup the LLM agent with defined tools and given models.
    Following Singleton pattern to not re-initialise the agent
    """
    global _llm_agent

    if _llm_agent is None:
        # Define tools
        tools = [
            Tool(
                name="Stock Data",
                func=lambda ticker: get_stocks_data(ticker),
                description="Get historical stock data for a given ticker symbol.",
            ),
            Tool(
                name="Stock Analysis",
                func=lambda ticker, analysis_type: stock_analysis(ticker, analysis_type),
                description="Get basic stock analysis.",
            ),
        ]

        # Initialize the LLM model
        llm_model = ChatGroq(model=model)

        # Initialize the agent
        _llm_agent = initialize_agent(
            llm=llm_model,
            tools=tools,
        )

    return _llm_agent


def query_stock_agent(question: str, ticker: str) -> str:
    """Send a query to the llm agent and return the result."""

    agent = setup_agent()
    #full_input = f"{question} (Ticker: {ticker})"

    prompt = f"""
        You are a stock query assistant. Please answer the following question about the stock symbol provided.
        Ticker: {ticker}
        Question: {question}
        Using the tools given.
        """
    try:
        answer = agent.run(prompt)
        # answer = agent.run(input=question, context=ticker)

        return answer
    except Exception as e:
        raise AgentException(f"Error in agent run: {str(e)}")


if __name__ == '__main__':
    # Test
    agent_response = query_stock_agent("What is the highest stock price of AAPL in the last year?", "AAPL")
    print(agent_response)


