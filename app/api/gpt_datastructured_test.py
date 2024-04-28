from openai import OpenAI
import json


def generate_description(raw_message):
    with open('../../config/settings.json', 'r') as config_file:
        config = json.load(config_file)

    client = OpenAI(api_key=config['openAI_api']['key'])

    messages = [{"role": "system",
                 "content": """
    **FIRST TASK**
    As a Data Structurer, verify and extract the corresponding data to fill up (if data provided) the data structure expressed with the described bellow json format.
    This data comes from Mercedes-Benz customers and is related to Mercedes-Benz electric cars."""},
                {"role": "system", "content": """
    **MAIN TASK**: 1) PROVIDE TWO STRUCTURED JSON OUTPUTS ( for **FIRST TASK** and **SECOND TASK** ) THAT CORRESPOND TO EACH JSON FORMAT EXAMPLE TEMPLATES SPECIFIED IN FURTHER PROMPTS. 2) PROVIDE A FLAG VERABLE, CALLED READY,(**FLAF VAR**) THAT SPECIFIES, THAT THERE IS ENOUGH DATA TO GIVE A RECOMENDATION. IT CAN HAVE EATHER VALUE true OR false.READY = true if is at least 50% of parameters are set or if name of the car is specified, set and corresponds to the provided names in parantethes(AND it correspond to one of the following names in parentheses(EQE 300
EQE 350
EQE 350 4MATIC
EQE 500 4MATIC
Mercedes-AMG EQE 43 4MATIC
EQS 450 4MATIC
EQS 450+
EQS 500 4MATIC
EQS 580 4MATIC
Mercedes-AMG EQS 53 4MATIC+
EQA 250
EQA 300 4MATIC
EQA 350 4MATIC
EQB 250+
EQB 300 4MATIC
EQB 350 4MATIC
EQT 200 standard
EQV 250 Lang
G-Klasse
Maybach EQS SUV
EQS 450 4MATIC SUV
EQS 500 4MATIC SUV
EQS 580 4MATIC SUV
EQE 300 SUV
EQE 350 4MATIC SUV
EQE 500 4MATIC SUV
AMG EQE 43 4MATIC SUV
AMG EQE 53 4MATIC+ SUV):).
    2) YOUR ANSWER MUST NOT CONTAIN ANY OTHER INFORMATION LIKE “YES, SURE” or "structure with VALUES, structure with WIGHTS" ETC., ONLY THIS TWO JSON STRUCRURES. 3) YOU MUST SPECIFY A CERTAIN VALUE TO EACH PARAMETER, NOT A RANGE. 5) PARAMETER'S VALUE ALLIGNED IN RANGE FORM 1 TO 10 DOES NOT CORRESPOND TO IT's WEIGHT 4) YOU CAN'T GO OUT OF RANGES AND MUST ALWAYS CONSIDER INFORMATION PROVIDED IN THE PARAMETER DESCRIPTION:
    """}, {"role": "system",
           "content": """
    **FIRST TASK**
    1. Provide json structure with VALUES:
    a) Template:
    
    {
    “name": "Mercedes",
    "horsepower": 245,
    "priceMin": 76076.70,
    "priceMax": 89160.70,
    "consumption": 17100,
    "range": 603,
    "rangeIn": 674,
    "seats": 4,
    "chargeTime": 32,
    "is4Matic": false,
    "size": 10 (,
    "globalRange": 20,
    "budget": 1000,
    }
    b) Behevioure in case the user didn't specified some parameter's value AND it's value doesn't logically emerges from the other:
    For Boolean: value = false
    For Numerical: value = null
    c) Parameter description:
    - name:
        1) Customer specified the parameter precisely AND it correspond to one of the following names in parentheses(EQE 300
EQE 350
EQE 350 4MATIC
EQE 500 4MATIC
Mercedes-AMG EQE 43 4MATIC
EQS 450 4MATIC
EQS 450+
EQS 500 4MATIC
EQS 580 4MATIC
Mercedes-AMG EQS 53 4MATIC+
EQA 250
EQA 300 4MATIC
EQA 350 4MATIC
EQB 250+
EQB 300 4MATIC
EQB 350 4MATIC
EQT 200 standard
EQV 250 Lang
G-Klasse
Maybach EQS SUV
EQS 450 4MATIC SUV
EQS 500 4MATIC SUV
EQS 580 4MATIC SUV
EQE 300 SUV
EQE 350 4MATIC SUV
EQE 500 4MATIC SUV
AMG EQE 43 4MATIC SUV
AMG EQE 53 4MATIC+ SUV):
            => value = specified value
             => "ready": true
        2) OTHERWISE value = "Mercedes"
    - Horsepower:
    Range: [100;600]
        1) Customer specified the parameter precisely:
            => value = specified value
        2) Customer specified the parameter, but not precisely:
            a) Customer wants powerful car: value is in range 400 - 600.
            b) Customer wants average car: value is in range 300 - 400.
            c) Customer wants quite and economical car: value is in range 100 — 300.
    - PriceMin:
    Range: [40000;200000]
    Customer specified the parameter precisely:
    => value = specified value
    Customer specified the parameter, but not precisely:
    a) Customer has a low minimum price preference: value is in range $40,000 - $75,000.
    b) Customer has a medium minimum price preference: value is in range $75,001 - $120,000.
    c) Customer has a high minimum price preference: value is in range $120,001 - $200,000.
    - PriceMax:
    Range: [40000;200000]
    Customer specified the parameter precisely:
    => value = specified value
    Customer specified the parameter, but not precisely:
    a) Customer has a low maximum price preference: value is in range $40,000 - $75,000.
    b) Customer has a medium maximum price preference: value is in range $75,001 - $120,000.
    c) Customer has a high maximum price preference: value is in range $120,001 - $150,000.
    - Consumption:
    Range: [15000;23000]
    (How much W/100km does the car consume)
    Customer specified the parameter precisely:
    => value = specified value
    Customer specified the parameter, but not precisely:
    a) Customer prefers a highly efficient car: value is in range 15000 - 17000.
    b) Customer prefers an average efficiency car: value is in range 17000 - 20000.
    c) Customer prefers a less efficient car: value is in range 20000 - 23000.
    - RangeIn:
    Range: [300;760]
    (Range in town)
    Customer specified the parameter precisely:
    => value = specified value
    Customer specified the parameter, but not precisely:
    a) Customer prefers a short-range car indoors: value is in range 300 - 440.
    b) Customer prefers a medium-range car indoors: value is in range 440 - 600.
    c) Customer prefers a long-range car indoors: value is in range 600 - 760.
    - Range:
    Range: [270;750]
    (Range on the highways)
    Customer specified the parameter precisely:
    => value = specified value
    Customer specified the parameter, but not precisely:
    a) Customer prefers a short-range car indoors: value is in range 270 - 380.
    b) Customer prefers a medium-range car indoors: value is in range 380 - 560.
    c) Customer prefers a long-range car indoors: value is in range 560 - 750.
    - Seats:
    Range: [4;10]
    Customer specified the parameter precisely:
    => value = specified value
    Customer specified the parameter, but not precisely:
    a) Customer wants a small car: value is in range 2 - 4 seats.
    b) Customer wants a medium-sized car: value is in range 5 - 7 seats.
    c) Customer wants a large car: value is in range 7 - 10 seats.
    - ChargeTime:
    Range: [30;45]
    Customer specified the parameter precisely:
    => value = specified value
    Customer specified the parameter, but not precisely:
    a) Customer wants a fast-charging car: value is in range 30 - 35 minutes.
    b) Customer wants an average-charging car: value is in range 35 - 40 minutes.
    c) Customer wants a slow-charging car: value is in range 40 - 45 minutes.
    - Is4Matic:
    Customer specified the parameter:
    a) Customer prefers a car with 4MATIC: value is true.
    b) Customer prefers a car without 4MATIC: value is false.
    c) Not defined => true if emerges from other requirements, otherwise null
    - Size:
    Range: [4;10]
    Customer specified the parameter precisely:
    => value = specified value
    Customer specified the parameter, but not precisely:
    a) Customer wants a compact car: value is 4.
    b) Customer wants a mid-size car: value is in range 5 - 7.
    c) Customer wants a big car: value is in range 8 - 10.
    - GlobalRange:
    Range: [1;10]
    (Specifies wether the customer prefers to ride in town or in village, farm area)
    Customer specified the parameter precisely:
    => value = specified value
    Customer specified the parameter, but not precisely:
    a) Customer wants a car for a farm: value is in range 1 - 3.
    b) Customer wants a car for a village: value is in range 4 - 6.
    c) Customer wants a car for a town: value is in range 7 - 10.
    - Budget:
    Range: [20000;220000]
    Customer specified the parameter precisely:
    => value = specified value
    Customer specified the parameter, but not precisely:
    a) Customer has a low budget: value is in range 40000 - 60000.
    b) Customer has a medium budget: value is in range 60000 - 90000.
    c) Customer has a high budget: value is in range 90000 - 220000.
    """}, {"role": "system", "content": """
    **SECOND TASK**
    2. Provide json structure with WEIGHTS:
    Weights represents the degree of customers preference in each parameter:
    1. Customer specified a parameter explicitly and precise 
        => weight is 10
    2. Customer mentioned the parameter, but not precisely
        => weight is in range 8 - 9
    3. Customer didn’t mentioned the parameter, but it emerges from other parameters
        => weight is in range 3 - 7
    4. Customer didn’t mentioned the parameter, and it can not be emerged from other parameters
        => weight is in range 0 - 2
    //YOUR SECOND ANSWER TEMPLATE START (ALWAYS INCLUDE IT)
    {
    “horsepower": 2,
    "priceMin": 1,
    "priceMax": 4,
    "consumption": 5,
    "range": 2,
    "rangeIn": 4,
    "seats": 10,
    "chargeTime": 4,
    "is4Matic": 9,
    "size": 8,
    "globalRange": 1,
    "budget": 2,
    }
    """}, {"role": "system", "content": """
    **FLAG VAR**
    Flag var example:
    //YOUR THIRD ANSWER EXAMPLE START
    1)Consider 50% of parameters aren't set to null
    "ready": true
    2)Consider 50% of parameters are set to null
    "ready": false
    3)Consider the name of the car is specified AND it correspond to one of the following names in parentheses(EQE 300
EQE 350
EQE 350 4MATIC
EQE 500 4MATIC
Mercedes-AMG EQE 43 4MATIC
EQS 450 4MATIC
EQS 450+
EQS 500 4MATIC
EQS 580 4MATIC
Mercedes-AMG EQS 53 4MATIC+
EQA 250
EQA 300 4MATIC
EQA 350 4MATIC
EQB 250+
EQB 300 4MATIC
EQB 350 4MATIC
EQT 200 standard
EQV 250 Lang
G-Klasse
Maybach EQS SUV
EQS 450 4MATIC SUV
EQS 500 4MATIC SUV
EQS 580 4MATIC SUV
EQE 300 SUV
EQE 350 4MATIC SUV
EQE 500 4MATIC SUV
AMG EQE 43 4MATIC SUV
AMG EQE 53 4MATIC+ SUV):
    "ready": true

    """}, {"role": "user",
           "content": "I'm in the market for an electric car that's sleek, fast, and has all the latest tech features. Price isn't a huge concern, but I don't want to break the bank. I need something with enough range to handle my daily commute and occasional road trips."},
                {"role": "assistant", "content": """
{
"configuration": {
"name": "Mercedes",
"horsepower": 400,
"priceMin": 100000,
"priceMax": 60000,
"consumption": null,
"range": 400,
"rangeIn": 500,
"seats": null,
"chargeTime": null,
"is4Matic": null,
"size": null,
"globalRange": 8,
"budget": 70000
},
"weights": {
"horsepower": 9,
"priceMin": 6,
"priceMax": 8,
"consumption": 0,
"range": 8,
"rangeIn": 9,
"seats": 0,
"chargeTime": 0,
"is4Matic": 0,
"size": 0,
"globalRange": 7,
"budget": 2
},
"ready": true
}
"""}, {"role": "user",
       "content": "I'm an eco-conscious consumer looking for an electric car with a focus on sustainability. It should have a minimal carbon footprint and be made from recycled materials where possible. Range and price are secondary considerations for me."
       }, {"role": "assistant", "content": """
}
"configuration": {
"name": "Mercedes",
"horsepower": null,
"priceMin": null,
"priceMax": null,
"consumption": 20000,
"range": null,
"rangeIn": null,
"seats": null,
"chargeTime": null,
"is4Matic": null,
"size": null,
"globalRange": null,
"budget": null
},
"weights": {
"horsepower": 0,
"priceMin": 0,
"priceMax": 0,
"consumption": 10,
"range": 0,
"rangeIn": 0,
"seats": 0,
"chargeTime": 0,
"is4Matic": 0,
"size": 0,
"globalRange": 0,
"budget": 0
},
"ready": false
}
"""}, {"role": "user",
       "content": "I'm a tech enthusiast looking for an electric car with the latest connectivity options and autonomous driving capabilities. Performance is important to me, so I want something with high horsepower and fast acceleration. Price is not a concern."},
                {"role": "assistant", "content": """
{
"configuration": {
"name": "Mercedes",
"horsepower": 600,
"priceMin": 200000,
"priceMax": 150000,
"consumption": null,
"range": null,
"rangeIn": null,
"seats": null,
"chargeTime": null,
"is4Matic": null,
"size": null,
"globalRange": null,
"budget": 200000
},
"weights": {
"horsepower": 9,
"priceMin": 6,
"priceMax": 8,
"consumption": 0,
"range": 0,
"rangeIn": 0,
"seats": 0,
"chargeTime": 0,
"is4Matic": 0,
"size": 0,
"globalRange": 0,
"budget": 2
},
"ready": false
}
"""}, {"role": "user", "content": f"{raw_message}"}]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.1,
        max_tokens=250,
        presence_penalty=0.5
    )
    reply = completion.choices[0].message.content
    return reply


def main_test():

    print(generate_description(
          "I want to by EfdQsdds"
         )
    )


 # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_test()

