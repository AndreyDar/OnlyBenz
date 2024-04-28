import json
import time
import traceback

from openai import OpenAI
import gradio as gr
import os

from app.api.gpt_datastructured_test import generate_description
from app.api.gpt_wrap_up import generate_wrapup
from app.preprocess import matchCars, get_matching_names, get_links

# Load CSS styles from styles.css


# Define the initial context for ChatGPT acting as a knowledgeable car dealer for Mercedes EQ cars
initial_context = "You are a knowledgeable car dealer for Mercedes-Benz, specializing in cars. Your goal is to guide customers in choosing the best car for their needs, emphasizing the benefits of electric cars. And you need to suggest EQ Mercedes cars to the users, as if it is really the best line of cars suiting them. An you must be friendly. And before suggesting any car models you need to know what size of the car the user want, for what does he need a car, will he use it for riding to work or for anything else, and only when you have enough data you can make an assumption about the best suitting car. And when a user says he wants to buy any car that is not electric, try to convice him of buying an electric car"

# Define the conversation history
conversation_history = []
isReadToGetLink = False
# Function to craft a message list for the API call
def create_message_list(history, user_input):
    message_list = [{"role": "system", "content": initial_context}]
    message_list.extend(history)
    message_list.append({"role": "user", "content": user_input})
    return message_list

# Function that manages the conversation
def chat_with_gpt(user_input):
    global conversation_history
    global isReadToGetLink
    with open('config/settings.json', 'r') as config_file:
        config = json.load(config_file)
    response = ""
    responseFromChat = False
    isObtainedLink = False


    client = OpenAI(api_key=config['openAI_api']['key'])
    
    # Create the list of messages for the API call
    messages = create_message_list(conversation_history, user_input)

    # time.sleep(0.05)
    description = generate_description(user_input)
    print(description)
    try:
        checkLink = generate_wrapup(user_input)
        print("checkLink->")
        print(checkLink)
        if(isReadToGetLink):
            json_resp = json.loads(checkLink)
            if(not (json_resp.get('anyMatches') is None) and not (json_resp.get('chosenCars') is None)):
                print("A link coms")
                print(json_resp)
                if(json_resp.get('anyMatches')):
                    response = get_links(json_resp.get('chosenCars'))
                    isObtainedLink = True

        if(not isObtainedLink):
            json_resp = json.loads(description)

            possibleNames = ("EQE 350", "EQE 500", "EQE 43", "EQS 450", "EQS 500", "EQS 580", "EQS 53", "EQA 250", "EQA 300",
                             "EQA 350", "EQB 250", "EQB 300", "EQB 350", "EQT 200", "EQV 250", "G-Klasse", "Maybach", "EQS 450",
                             "EQS 500", "EQS 580", "EQE 300", "EQE 350", "EQE 500", "EQE 43", "EQS 450")
            if(len(response) == 0):
                if(not (json_resp.get('configuration') is None) and not (json_resp.get('weights') is None) and not (json_resp.get('ready') is None)):
                    if json_resp.get('ready'):
                        nameToExtract = ""
                        print("good")
                        for name in possibleNames:
                            if name in json_resp.get('configuration').get('name'):
                                nameToExtract = name
                        if len(nameToExtract) == 0:
                            response = str(matchCars(json_resp.get('weights'), json_resp.get('configuration')))
                            isReadToGetLink = True
                        else:
                            response = str(get_matching_names(nameToExtract))
                            isReadToGetLink = True
                    else:
                        responseFromChat = True
                else:
                    responseFromChat = True
    except Exception:
        print(traceback.format_exc())
        print("JSON exception")
        responseFromChat = True

        #json cheeeeeck

        # Call the OpenAI API with the conversation history
    print("responseFromChat: " + str(responseFromChat))
    if responseFromChat:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature= 1,
            messages=messages
        )

        # Extract the assistant's message from the response
        response = response.choices[0].message.content


    if isObtainedLink:
         response_gpt = client.chat.completions.create(
             model="gpt-3.5-turbo",
             temperature=1,
             messages=messages
         )

         # Extract the assistant's message from the response
         response = response_gpt.choices[0].message.content + "\n" + response

    
    # Update conversation history
    conversation_history.append({"role": "assistant", "content": response})
    
    # If a recommendation is made, append a URL to the configurator. This is a placeholder logic.
    if "recommendation" in response.lower():
        response += "\nYou can configure your Mercedes EQ car here: [Mercedes EQ Configurator](https://www.mercedes-benz.com/en/vehicles/configurator/#/main/car)"





    return response, conversation_history


