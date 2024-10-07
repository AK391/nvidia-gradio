import gradio as gr
import nvidia_gradio  

gr.load(
    name='meta/llama-3.1-405b-instruct',  
    src=nvidia_gradio.registry,
    title='NVIDIA NIM-Gradio Integration',
    description="Chat with NVIDIA's NIM LLaMA 3.1 405B Instruct model.",
    examples=["Explain quantum gravity to a 5-year old.", "How many R are there in the word Strawberry?"]
).launch()