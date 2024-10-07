import os
from openai import OpenAI
import gradio as gr
from typing import Callable

__version__ = "0.0.1"


def get_fn(model_name: str, preprocess: Callable, postprocess: Callable, api_key: str):
    def fn(message, history):
        inputs = preprocess(message, history)
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )
        completion = client.chat.completions.create(
            model=model_name,
            messages=inputs["messages"],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=True,
        )
        response_text = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                delta = chunk.choices[0].delta.content
                response_text += delta
                yield postprocess(response_text)

    return fn


def get_interface_args(pipeline):
    if pipeline == "chat":
        inputs = None
        outputs = None

        def preprocess(message, history):
            messages = []
            for user_msg, assistant_msg in history:
                messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": assistant_msg})
            messages.append({"role": "user", "content": message})
            return {"messages": messages}

        postprocess = lambda x: x  # No post-processing needed
    else:
        # Add other pipeline types when they will be needed
        raise ValueError(f"Unsupported pipeline type: {pipeline}")
    return inputs, outputs, preprocess, postprocess


def get_pipeline(model_name):
    # Determine the pipeline type based on the model name
    # For simplicity, assuming all models are chat models at the moment
    return "chat"


def registry(name: str, token: str | None = None, **kwargs):
    """
    Create a Gradio Interface for a model on NVIDIA NIM.

    Parameters:
        - name (str): The name of the NVIDIA NIM model.
        - token (str, optional): The API key for NVIDIA NIM.
    """
    api_key = token or os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("NVIDIA_API_KEY environment variable is not set.")

    pipeline = get_pipeline(name)
    inputs, outputs, preprocess, postprocess = get_interface_args(pipeline)
    fn = get_fn(name, preprocess, postprocess, api_key)

    if pipeline == "chat":
        interface = gr.ChatInterface(fn=fn, **kwargs)
    else:
        # For other pipelines, create a standard Interface (not implemented yet)
        interface = gr.Interface(fn=fn, inputs=inputs, outputs=outputs, **kwargs)

    return interface