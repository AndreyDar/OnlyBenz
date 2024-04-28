from fastapi import APIRouter
import gradio as gr
import os

from app.api.chatgpt import chat_with_gpt

router = APIRouter()

@router.get("/")
async def read_root():
    return {"Hello": "World"}


with open("app/frontend/styles.css", "r") as file:
    css_styles = file.read()


# Create the Gradio interface
iface = gr.Interface(
    fn=chat_with_gpt,  # The main function to handle chat
    inputs=gr.Textbox(placeholder="How can I assist you today?", label="Your message", lines=2),
    outputs=[
        gr.Textbox(label="Car Dealer AI"),  # To show the AI's response
        gr.JSON(label="Conversation History", visible=False)  # To store the conversation history without showing it on the interface
    ],
    title="<span style='background: linear-gradient(90deg, #7FE786, #58A7FE); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 24px;'>OnlyBenz Chatbot Assistant</span>",
    description="I am your virtual car dealer assistant specializing in the Mercedes EQ electric car line. Let me help you find the perfect car!",
    theme="default",
    allow_flagging="never",
    examples=[
        ["Hi! I'm thinking about getting a new car and want to explore electric vehicles."]
    ],
    css=css_styles
)

# Launch the Gradio interface with the option to share it publicly
iface.launch(share=True)

# Note: The `css_style` can be defined as a string with CSS code as previously explained to customize the appearance.
