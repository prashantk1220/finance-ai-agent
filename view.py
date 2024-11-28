import gradio as gr
import requests


def query_backend(ticker, question):
    stock_resp = requests.get(f"http://127.0.0.1:8080/stock/{ticker}/highest-price")
    news_resp = requests.post("http://127.0.0.1:8080/query", json={"question": question})
    return stock_resp.json(), news_resp.json()


def gradio_ui():
    with gr.Blocks() as ui:
        gr.Markdown("## Finance Data Query")
        ticker = gr.Textbox(label="Ticker Symbol")
        question = gr.Textbox(label="Ask a question about the data")
        stock_output = gr.JSON(label="Stock Data")
        news_output = gr.JSON(label="News Insights")

        query_button = gr.Button("Query")
        query_button.click(query_backend, inputs=[ticker, question], outputs=[stock_output, news_output])

    ui.launch()


gradio_ui()
