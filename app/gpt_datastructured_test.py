import openai
import json

with open('../config/settings.json', 'r') as config_file:
    config = json.load(config_file)

openai.api_key = config['openAI_api']['key']  # Add your OpenAI API key here

def generate_description(input):
    messages = [
        {"role": "user",
         "content": """As a Data Structurer, verify and extract the corresponding data to fill up (not nececerally complete) the data structure expressed with the following json format (Disclaimer: I NEED ONLY STRUCTURED DATA, NO OTHER COMMENTS LIKE "YES, SURE AND SO FORCE"): {"preferences": {
    "body_style": "SUV",
    "range_preference": "300+ miles",
    "interior_color": "black",
    "technology_features": ["autonomous driving", "voice assistant"],
    "price_range": {
      "min_price": 60000,
      "max_price": 100000
    },
    "additional_features": [
      "panoramic sunroof", 
      "premium sound system"
    ]
  }}' \n"""},
    ]

    messages.append({"role": "user", "content": f"{input}"})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = completion.choices[0].message.content
    return reply

def main_test():
    print(generate_description("Hi! I'm interested in buying an electric car from Mercedes. Can you help me find one?; Sure! I'm looking for a sedan with a range of over 250 miles. I prefer a beige interior and I'm interested in autonomous driving and voice assistant technology. My budget is between $70,000 and $120,000. Also, I'd like it to have a panoramic sunroof and a premium sound system."))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_test()