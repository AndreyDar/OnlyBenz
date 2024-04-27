# import openai 
# import gradio

# openai.api_key = "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"

# # Database of EQ cars with their categories and capacities
# eq_cars_database = {
#     "luxury": {
#         "big": ["EQS", "EQS SUV"],
#         "middle": ["EQE", "EQE SUV"],
#         "small": ["EQC"]
#     },
#     "business": {
#         "big": ["EQS", "EQS SUV"],
#         "middle": ["EQE", "EQE SUV"],
#         "small": ["EQC"]
#     },
#     "economy": {
#         "big": ["EQS SUV"],
#         "middle": ["EQE", "EQE SUV"],
#         "small": ["EQC"]
#     }
# }

# def CustomChatGPT(user_input, messages=[], user_info={}):
#     try:
#         # Append user input to messages
#         messages.append({"role": "user", "content": user_input})
        
#         # Check if user is interested in Mercedes-Benz EQ models
#         if "EQ" in user_input or "electric" in user_input:
#             if not user_info:
#                 # Start asking low-key questions to gather user preferences
#                 assistant_response = "Hey there! Looking for an electric ride, huh? Let's find the perfect EQ car for you. Mind if I ask you a few chill questions?"
#                 user_info["segment"] = None
#                 user_info["capacity"] = None
#                 user_info["purpose"] = None
#                 user_info["distance_from_work"] = None
#             elif not user_info["segment"]:
#                 assistant_response = "Cool, let's keep it breezy. What segment of car are you into - luxury, business, or economy?"
#             elif not user_info["capacity"]:
#                 assistant_response = "Sweet! Now, how about the capacity - big, middle, or small?"
#             elif not user_info["purpose"]:
#                 assistant_response = "Got it! What's your main reason for needing a car - work commute, road trips, or something else?"
#             elif not user_info["distance_from_work"]:
#                 assistant_response = "Right on! Do you live far from your workplace?"
#             else:
#                 # All info collected, recommend the best-suited EQ car
#                 segment = user_info["segment"]
#                 capacity = user_info["capacity"]
#                 purpose = user_info["purpose"]
#                 distance_from_work = user_info["distance_from_work"]
                
#                 if segment in eq_cars_database and capacity in eq_cars_database[segment]:
#                     available_cars = eq_cars_database[segment][capacity]
#                     # Recommend the first available car from the database
#                     recommended_car = available_cars[0]
#                     assistant_response = f"Based on your preferences, I'd recommend the {recommended_car}! It's a great choice for your needs."
#                 else:
#                     assistant_response = "Hmm, it seems we don't have a perfect match for your preferences. Let me see what I can do."
#         else:
#             completion = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=messages  
#             )
#             assistant_response = completion.choices[0].message.content
        
#         return assistant_response.strip(), user_info
#     except Exception as e:
#         return "An error occurred: {}".format(str(e)), user_info

# # Launch the Gradio interface
# demo = gradio.Interface(
#     fn=CustomChatGPT,
#     inputs="text",
#     outputs="text",
#     title="Mercedes-Benz EQ Assistant",
#     description="Ask me about electric cars or Mercedes-Benz EQ models.",
#     examples=[
#         ["I'm interested in buying an electric car."]
#     ]
# )
# demo.launch(share=True)


import openai 
import gradio

openai.api_key = "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"

class CarDealer:
    def __init__(self):
        self.user_info = {}
        self.questions = [
            "What class of car are you interested in? (e.g., luxury, business, economy)",
            "What capacity are you looking for? (e.g., big, middle, small)",
            "What will you primarily use the car for? (e.g., commuting, road trips, family outings)",
            "How far is your workplace from your home?"
        ]
        self.current_question = 0

    def next_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.current_question += 1
            return question
        else:
            return None

    def process_response(self, response):
        if self.current_question == 1:
            self.user_info["class"] = response
        elif self.current_question == 2:
            self.user_info["capacity"] = response
        elif self.current_question == 3:
            self.user_info["purpose"] = response
        elif self.current_question == 4:
            self.user_info["distance_from_work"] = response

    def recommend_car(self):
        # Assuming we have a database of EQ Mercedes cars categorized by class and capacity
        eq_mercedes_cars = {
            "luxury": {"big": "EQS", "middle": "EQE", "small": "EQC"},
            "business": {"big": "EQS", "middle": "EQE", "small": "EQC"},
            "economy": {"big": "EQS SUV", "middle": "EQE", "small": "EQC"}
        }

        car_class = self.user_info.get("class")
        capacity = self.user_info.get("capacity")

        if car_class and capacity:
            recommended_car = eq_mercedes_cars.get(car_class, {}).get(capacity)
            if recommended_car:
                return f"Based on your preferences, I'd recommend the {recommended_car}!"
            else:
                return "It seems we don't have a perfect match for your preferences."
        else:
            return "I need more information to recommend a car. Can you please answer a few more questions?"

dealer = CarDealer()

def CustomChatGPT(user_input):
    try:
        if user_input.strip() == "":
            return "Sorry, I didn't catch that. Could you please provide a response?"

        # If there are more questions to ask
        if dealer.current_question < len(dealer.questions):
            question = dealer.next_question()
            return question

        # Process the user's response and recommend a car
        else:
            dealer.process_response(user_input)
            return dealer.recommend_car()

    except Exception as e:
        return "An error occurred: {}".format(str(e))

# Launch the Gradio interface
demo = gradio.Interface(
    fn=CustomChatGPT,
    inputs="text",
    outputs="text",
    title="Car Dealer Assistant",
    description="Welcome to our car dealership! Let's find the perfect EQ Mercedes car for you.",
    examples=[
        ["I'm interested in buying a car."]
    ]
)
demo.launch(share=True)
