import json

from openai import OpenAI
import gradio as gr
import os


# Load CSS styles from styles.css


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
    with open('config/settings.json', 'r') as config_file:
        config = json.load(config_file)

    client = OpenAI(api_key=config['openAI_api']['key'])
    
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


