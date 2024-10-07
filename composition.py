import gradio as gr
import nvidia_gradio  # Changed from anthropic_gradio to nvidia_gradio

with gr.Blocks() as demo:
    with gr.Tab("llama-3.2-3b-instruct"):
        gr.load('meta/llama-3.2-3b-instruct', src=nvidia_gradio.registry)
    with gr.Tab("Mixtral 8x7B"):
        gr.load('mistralai/mixtral-8x7b-instruct-v0.1', src=nvidia_gradio.registry)

demo.launch()