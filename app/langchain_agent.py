"""Module to Setup the agent and the tools"""

from langchain.agents import Tool, initialize_agent
from langchain_groq import ChatGroq
from app.utility import get_stocks_data, stock_analysis
import logging
import warnings

warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__)


class AgentException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class LLMAgent:
    def __init__(self, model: str = "llama3-8b-8192"):
        self.agent = self.setup_agent(model)

    @staticmethod
    def setup_agent(model):
        """
        Setup the LLM agent with defined tools and given model.
        """
        # Define tools
        tools = [
            Tool(
                name="Stock Data",
                func=lambda ticker: get_stocks_data(ticker),
                description="Get basic stock analysis.",
            ),
            Tool(
                name="Stock Analysis",
                func=lambda ticker, analysis_type=None: stock_analysis(ticker, analysis_type),
                description="Get basic stock analysis.",
            ),
        ]

        # Initialize the LLM model
        try:
            llm_model = ChatGroq(model=model)
        except Exception as e:
            raise AgentException(f"Failed to initialize ChatGroq model '{model}': {e}")

        # Initialize the agent
        try:
            llm_agent = initialize_agent(
                llm=llm_model,
                tools=tools,
            )
            return llm_agent
        except Exception as e:
            raise AgentException(f"Failed to initialize LLM agent: {e}")

    def query_stock_agent(self, question: str, ticker: str) -> str:
        """Send a query to the llm agent and return the result."""

        # full_input = f"{question} (Ticker: {ticker})"  # Experiment
        prompt = f"""
        You are a stock query assistant. Please answer the following question about the stock {ticker}:
        {question}
        Using the tools given and format your response in a clear and concise manner.
        """
        try:
            answer = self.agent.run(prompt)
            # answer = agent.run(input=question, context=ticker)

            return answer
        except Exception as e:
            raise AgentException(f"Error in agent run: {str(e)}")


if __name__ == '__main__':
    # Test
    agent = LLMAgent()
    agent_response = agent.query_stock_agent("What is the highest stock price of AAPL in the last year?", "AAPL")
    print(agent_response)
