from flask import session
import openai
import os

# Initialize OpenAI API key from environment variables
api_key = os.environ.get("OPENAI_API_KEY")

# Initialize the OpenAI API client
openai.api_key = api_key

def create_chat_completion(prompt, model="gpt-4", conversation_history=None, temperature=1, max_tokens=100):
    # """
    # Creates a chat completion using OpenAI's ChatGPT.

    # Parameters:
    # - prompt (str): The prompt or question to ask the model.
    # - model (str): The model to use for the chat completion. Default is "gpt-3.5-turbo".
    # - conversation_history (list): A list of previous messages in the conversation.
    # - temperature (float): Controls the randomness of the model's output.
    # - max_tokens (int): The maximum number of tokens for the model to generate.

    # Returns:
    # - str: The model's response.
    # """
     
    # Initialize the conversation history if it doesn't exist.
    if conversation_history is None:
        conversation_history = []
        
    # Check if it's the user's first time and if the purchase frequency is already set in the session.
    # THIS WILL BE CHANGED TO DB USE
    first_time_user = session.get('first_time_user', True)
    purchase_frequency = session.get('purchase_frequency', None)
    
    # If it's the user's first time, instruct ChatGPT to ask for the purchase frequency
    if first_time_user:
        session['first_time_user'] = False
        conversation_history.append({"role": "system", "content": "You are my inventory assistant. Please ask the user how often they purchase groceries."})
    
    # Always offer the option to change purchase frequency
    if purchase_frequency:
        conversation_history.append({"role": "assistant", "content": f"Your current purchase frequency is set to {purchase_frequency}. Would you like to change it?"})
    
    # Add the user's message to the conversation history
    conversation_history.append({"role": "user", "content": prompt})

    # Create the API request payload
    payload = {
        "model": model,
        "messages": conversation_history,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    # Make the API request
    response = openai.ChatCompletion.create(**payload)

    # Extract and return the model's message
    model_message = response['choices'][0]['message']['content']

    # Update the purchase frequency if the user chooses to set or change it
    if "purchase frequency" in model_message.lower():
        purchase_frequency = model_message.split(":")[-1].strip()
        session['purchase_frequency'] = purchase_frequency

    return model_message

