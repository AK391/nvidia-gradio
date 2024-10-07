import gradio as gr
import nvidia_gradio  # Changed from openai_gradio to nvidia_gradio


gr.load(
    name='meta/llama-3.1-405b-instruct',  # Updated to use a NVIDIA NIM model
    src=nvidia_gradio.registry,
).launch()