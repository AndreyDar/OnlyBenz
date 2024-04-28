from openai import OpenAI
import json


def generate_wrapup():
    with open('../../config/settings.json', 'r') as config_file:
        config = json.load(config_file)

    client = OpenAI(api_key=config['openAI_api']['key'])

    messages = [{"role": "system",
                 "content": """ **Instructions**
                            You are wrapping a dealer chatbot conversation with mercades-benz customer.
                            Your Task:
                             Given a list of names of electric cars(next message provided by the system), that are being suggested to the user
                              and given the names of cars chosen by the user(following message provided by the user) YOU NEED TO:
                              1) Compare the GIVEN CARS and CHOSEN CARS
                              2) Verify the metch (match, only if the at least one full name, i.e. every letter in it, matches)
                              3) If there is a mathe:
                                You need to substitute the example values(**EXAMPLE**) of the parameters listed in a json structure(**TAMPLATE**). The instruction to the substitution of example values and parameter description will be provided with a json structure sample.
                                **TEMPLATES**
                                {
                                "chosenCars" : [**EXAMPLE**, **EXAMPLE**,...]
                                "anyMatches" : true
                                }
                              4) If there are no mathes: 
                                Set "anyMatches" with false: 
                                {
                                "anyMatches" : false
                                }
                            """}, {"role": "system",
                 "content": """ 
                            EQS, EQB
                            """},
                {"role": "user",
                 "content": """ 
                                No, that's not what i wanted
                                """},
                {"role": "assistant",
                 "content": """ 
                            {
                                "anyMatches" : false
                            }
                            """}, {"role": "system",
                 "content": """ 
                            EQB
                            """},
                {"role": "user",
                 "content": """ 
                                EQA 300
                                """},
                {"role": "assistant",
                 "content": """ 
                            {
                                "anyMatches" : false
                            }
                            """}, {"role": "system",
                 "content": """ 
                            EQS
                            """},
                {"role": "user",
                 "content": """ 
                                EQS
                                """},
                {"role": "assistant",
                 "content": """ 
                            {
                                "chosenCars" : [EQS]
                                "anyMatches" : true
                            }
                            """}
                ]

    messages.append({"role" : "system", "content" : "EQA, EQS, EQB"})
    messages.append({"role": "user", "content": "EQB"})

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=250,
    )


    reply = completion.choices[0].message.content
    return reply


def main_test_1():
    print(generate_wrapup())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_test_1()

