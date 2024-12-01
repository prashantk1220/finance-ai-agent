import pytest
from unittest.mock import MagicMock, patch

from dotenv import load_dotenv

from app.langchain_agent import LLMAgent


@pytest.fixture
def llm_agent():
    load_dotenv()
    return LLMAgent()


def test_query_stock_agent(llm_agent):
    question = "What is the current stock price?"
    ticker = "AAPL"
    expected_response = "Mocked response"

    with patch.object(llm_agent, 'query_stock_agent', return_value=expected_response) as mock_run:
        response = llm_agent.query_stock_agent(question, ticker)
        mock_run.assert_called_once_with(question, ticker)
        assert response == expected_response
