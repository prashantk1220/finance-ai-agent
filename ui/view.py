import gradio as gr
import requests


def query_backend(question, ticker=None):
    """Requests the API service to fetch results from the AI Agent"""
    stock_resp = requests.post(f"http://localhost:8000/v1/query/{ticker}", json={"question": question})
    return stock_resp.json()


def validate_inputs(question, ticker):
    # Check if both fields are filled
    return gr.update(interactive=bool(question and ticker))


def gradio_ui():
    with gr.Blocks() as ui:
        gr.Markdown("## Finance Data Query")
        ticker = gr.Textbox(label="Ticker Symbol", placeholder="Enter the ticker symbol (e.g., AAPL)")
        question = gr.Textbox(label="Ask a question about the given ticker",
                              placeholder="e.g., What was the highest price last week?")
        stock_output = gr.JSON(label="Data")
        query_button = gr.Button("Query", interactive=False)  # Initially disabled

        # Add dynamic input validation
        ticker.change(validate_inputs, inputs=[question, ticker], outputs=[query_button])
        question.change(validate_inputs, inputs=[question, ticker], outputs=[query_button])

        # Query backend when button is clicked
        query_button.click(query_backend, inputs=[question, ticker], outputs=[stock_output])

    ui.launch()
    return ui


gradio_ui()
