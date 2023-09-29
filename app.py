import gradio as gr
from main_scraping import main

iface = gr.Interface(fn=main, inputs="text", outputs="text")
iface.launch()