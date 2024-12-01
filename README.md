# Finance-AI-Agent

This repository contains a FastAPI application incorporating a LangChain Agent.
It utilses LLM model to answer queries on financial data analysis. 
 

## Table of Contents

- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [UI Screenshot](#ui-screenshot)
- [Trade-offs Made](#trade-offs)
- [Makefile Commands](#makefile-commands)

---


## System Architecture

Below is the high-level system architecture of the project. For more details, refer to the [System Architecture Document](docs/component-diagram.pdf).

![System Architecture](docs/system-architecture-thumbnail.png)


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/prashantk1220/finance-ai-agent.git
   cd finance-ai-agent
   ```
   
2. Use the Makefile commands to Install all the required libraries.
   Prerequistie: The system should have Python3.9 or above installed. 
    ```
   make install
   ```
  

## Usage

Run the below command after the installation. 
Prerequisite: The database should be working and accepting connections on the port defined in env file.
```
make run
```

Launch the UI using another terminal with:
```
make ui
```

### Backend 
After running `make run`, the FastAPI backend is available at:
 * **Swagger UI**: http://127.0.0.1:8080/docs 
 
### UI 
After running `make ui`, the Gradio UI will be available at:
 * **Gradio UI**: http://127.0.0.1:7860”

Use the UI for your queries. 


## UI Screenshots

Here are some working example screenshots of the Gradio-powered UI:

![User Interface](docs/ui-screenshot.png) 


Makefile Commands 
-----------------

The `Makefile` simplifies common tasks for this project. Below is a list of the most important commands:

| Command         | Description                                           |
|-----------------|-------------------------------------------------------|
| `make install`  | Install all required dependencies.                    |
| `make test`     | Run the test suite using `pytest`.                    |
| `make run`      | Launch the FastAPI application.                       |
| `make all`      | Runs all the above cmds in sequence.                                  |
| `make ui`       | Start the Gradio UI.                                  |
| `make clean`    | Remove Python cache files and test artifacts.         |
| `make help`     | Display the commands available.         |



Trade-offs Made
----------------

- Database schema was chosed based on one table for all the stock data, vs multiple tables per ticker.
 This design helps manage queries and table efficiently, while scaling can be attained by partitioning the table based on tickers column as the data grows.

- LLM Agent queries the database directly than using API endpoints, which makes it tightly coupled system,
but it improves the response time by eliminating the network latency. 
Also this adds scope for introducing SQLQueryBased tools for the Agent.
 


Further Improvements 
----------------- 

- LLM Agent Prompts can be experimented for better results
- Additional Tools can be configured for the AI Agent
- Robust Integration tests
- The API can utilised for caching of frequently queried data
- More information in [Improvements-doc](docs/improvements.txt)
