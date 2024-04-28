from openai import OpenAI
import gradio as gr
import os

client = OpenAI(

    api_key="sk-..."
)


# Load CSS styles from styles.css
with open("styles.css", "r") as file:
    css_styles = file.read()

# Define the initial context for ChatGPT acting as a knowledgeable car dealer for Mercedes EQ cars
initial_context = "You are a knowledgeable car dealer for Mercedes-Benz, specializing in cars. Your goal is to guide customers in choosing the best car for their needs, emphasizing the benefits of electric cars. And you need to suggest EQ Mercedes cars to the users, as if it is really the best line of cars suiting them. An you must be friendly. And before suggesting any car models you need to know what size of the car the user want, for what does he need a car, will he use it for riding to work or for anything else, and only when you have enough data you can make an assumption about the best suitting car. And when a user says he wants to buy any car that is not electric, try to convice him of buying an electric car"

# Define the conversation history
conversation_history = []

# Function to craft a message list for the API call
def create_message_list(history, user_input):
    message_list = [{"role": "system", "content": initial_context}]
    message_list.extend(history)
    message_list.append({"role": "user", "content": user_input})
    return message_list

# Function that manages the conversation
def chat_with_gpt(user_input):
    global conversation_history
    
    # Create the list of messages for the API call
    messages = create_message_list(conversation_history, user_input)
    
    # Call the OpenAI API with the conversation history
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature= 1, 
        messages=messages
    )

    # Extract the assistant's message from the response
    assistant_response = response.choices[0].message.content
    
    # Update conversation history
    conversation_history.append({"role": "assistant", "content": assistant_response})
    
    # If a recommendation is made, append a URL to the configurator. This is a placeholder logic.
    if "recommendation" in assistant_response.lower():
        assistant_response += "\nYou can configure your Mercedes EQ car here: [Mercedes EQ Configurator](https://www.mercedes-benz.com/en/vehicles/configurator/#/main/car)"
    
    return assistant_response, conversation_history

# Reset the conversation (you can bind this to a button in the interface)
def reset_conversation():
    global conversation_history
    conversation_history = []

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
