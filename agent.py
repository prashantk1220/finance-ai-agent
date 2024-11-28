import yfinance as yf
from langchain.agents import Tool
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_react_agent


from dotenv import load_dotenv

load_dotenv()

# Helper functions
def get_stock_data(ticker):
    """Fetch stock data for a given ticker."""
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    return hist


def stock_analysis(ticker, analysis_type):
    """Perform basic analytics on stock data."""
    hist = get_stock_data(ticker)
    if analysis_type == "highest":
        return f"The highest stock price of {ticker} is {hist['High'].max()}"
    elif analysis_type == "average":
        return f"The average stock price of {ticker} is {hist['Close'].mean()}"
    else:
        return "Invalid analysis type. Use 'highest' or 'average'."


# Tools
tools = [
    Tool(name="Get Stock Data", func=get_stock_data, description="Fetch stock data for a given ticker."),
    Tool(name="Stock Analysis", func=stock_analysis, description="Perform basic analytics on stock data."),
]



# Initialize the LLM
llm = OpenAI(temperature=0, model="text-davinci-003")

# Define tools
tools = [
    Tool(
        name="Stock Data",
        func=lambda ticker: get_stock_data(ticker),
        description="Get historical stock data for a given ticker symbol.",
    ),
    Tool(
        name="Stock Analysis",
        func=lambda ticker, analysis_type: stock_analysis(ticker, analysis_type),
        description="Get basic stock analysis.",
    ),
]


# Create a React-based agent
memory = ConversationBufferMemory(memory_key="chat_history")
agent = create_react_agent(
    llm=llm,
    tools=tools
)

# Example usage
response = agent.run("Show me the stock price chart for AAPL")
print(response)


# Interaction with the agent
if __name__ == "__main__":
    print("Welcome to the Stock and News Agent!")
    while True:
        user_query = input("\nEnter your query (or 'exit' to quit): ")
        if user_query.lower() == "exit":
            print("Goodbye!")
            break
        response = agent.run(user_query)
        print(response)

