import pytest
from unittest.mock import MagicMock, patch
from app.langchain_agent import query_stock_agent


@pytest.mark.parametrize(
    "question, ticker, mock_response",
    [
        ("What is the highest stock price of AAPL in the last year?", "AAPL", "The highest stock price of AAPL is $180."),
        ("What is the lowest stock price of MSFT in the last year?", "MSFT", "The lowest stock price of MSFT is $220."),
    ],
)
def test_query_stock_agent(question, ticker, mock_response):
    """
    Test the query_stock_agent function with mocked agent responses.
    """
    with patch("app.langchain_agent._llm_agent") as mock_agent:
        mock_agent.run = MagicMock(return_value=mock_response)

        # Call the function
        response = query_stock_agent(question, ticker)

        # Assertions
        mock_agent.run.assert_called_once_with(input=question, context=ticker)
        assert response == mock_response
