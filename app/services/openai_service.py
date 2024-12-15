import openai
from typing import List
from app.models import Message
from app.config import settings


class OpenAIService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def get_chat_response(self, prompt: str, history: List[Message] = None) -> str:
        messages = []
        # start_prompt = "Welcome, Leo! You are the friendly and helpful of AAP seller, here to assist customers with their inquires. Your main task is to provide support to customer and understand what products they want to buy from you." \
        #             "industry are they looking to purchase or gather more information. " \
        #             "When interacting, listen carefully for cues about the customer's mood and the context of their questions. " \
        #             "For complex queries that require detailed explanations, break down your responses into simple, easy-to-follow steps. Your goal is to make every customer feel heard, supported, and satisfied with the service. " \
        #             "**Key Instructions for Interactions:" \
        #             "1. **Clarity Precision:** Use clear and precise language to avoid misunderstandings. If a concept is complex, simplify it without losing the essence. " \
        #             "3. **Feedback Queries:** Occasionally ask for feedback to confirm the customer is satisfied with the solution or needs further assistance. " \
        #             "** Few Scenarios ** 1 If they are looking to purchase a product: " \
        #             "- Ask details about the product like what the product name is. any specifications they want to provide. " \
        #             " - Ask for high level specifications needed." \
        #            " - Once the details are captured move on to next questions." \
        #            "- Ask the quantity looking to purchase " \
        #             "- Ask the time frame they want to receive ? " \
        #            "- Then respond by mentioning that you have taken details and would get back to them. ** " \
        #            "** 2 If they are looking to inquire about a product: " \
        #             "-  Ask details about the product like what the product name is, any specifications they want to provide? " \
        #             "-  Ask for phone number or email to reach back? " \
        #             "- Then respond by mentioning that you have taken details and would get back to them. **" \
        #             "Your role is crucial in making AAP Seller' customer support experience outstanding. If there are multiple questions to be asked, start asking with one question at a time. " \
        #                "The answer is a sms message, so it needs to be brief and clear. " \
        #                "You should avoid mentioning buying from other places. "
        # Add chat history if available

        # my_prompt = "You are a Sales Agent and need to gather information from the customer. Answer the user question based on previous context. The answer is a sms message, so it needs to be brief and clear. Once you have the details, notify then by thanking to reach out and we will get back to them : " + prompt
        my_prompt = "I am a Sale procurement analyst in a hardware company and looking to get more information. Add a newline character for new paragraphs or if answer contains number 1,2,3 to render new line on a web page.Question:" + prompt
        if history:
            print("history length", len(history))
            for msg in history:
                print(msg)
                message = Message.parse_raw(msg)
                messages.append({
                    "role": message.role,
                    "content": message.content
                })

        # Add current prompt
        # if history:
        messages.append({
            "role": "user",
            "content": my_prompt
        })
        # else:
        #     messages.append({
        #         "role": "user",
        #         "content": start_prompt
        #     })
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
