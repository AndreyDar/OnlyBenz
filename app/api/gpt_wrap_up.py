from openai import OpenAI
import json


def generate_wrapup(raw_message):
    with open('config/settings.json', 'r') as config_file:
        config = json.load(config_file)

    client = OpenAI(api_key=config['openAI_api']['key'])

    messages = [{"role": "system",
                 "content": """ **Instructions**
                            You are wrapping a dealer chatbot conversation with mercades-benz customer.
                            Your Task:
                             Given a list of names of electric cars(next message provided by the system), that are being suggested to the user
                             YOU NEED TO:
                              1) Verify the match:
                                    There is a match if the user explicitly specified the car name he wants. Otherwise there is no match
                              2) If there is a match:
                                You need to substitute the example values(**EXAMPLE**) of the parameters listed in a json structure(**TAMPLATE**). The instruction to the substitution of example values and parameter description will be provided with a json structure sample.
                                **TEMPLATES**
                                {
                                "chosenCars" : ["**EXAMPLE**", "**EXAMPLE**",...],
                                "anyMatches" : true
                                }
                              3) If there are no mathes: 
                                Set "anyMatches" with false: 
                                {
                                "anyMatches" : false
                                }
                            """},
                {"role": "user",
                 "content": """ 
                                No, that's not what I wanted
                                """},
                {"role": "assistant",
                 "content": """ 
                            {
                                "anyMatches" : false
                            }
                            """},
                {"role": "user",
                 "content": """ 
                                Yes, I lowe this car!
                                """},
                {"role": "assistant",
                 "content": """ 
                            {
                                "anyMatches" : false
                            }
                            """},
                {"role": "user",
                 "content": """ 
                                EQS
                                """},
                {"role": "assistant",
                 "content": """ 
                            {
                                "chosenCars" : ["EQS"],
                                "anyMatches" : true
                            }
                            """}
                ]

    messages.append({"role": "user", "content": f"{raw_message}"})

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.1,
        max_tokens=250,
    )




    reply = completion.choices[0].message.content
    return reply


def main_test_1():
    print(generate_wrapup("I love EQS"))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_test_1()

