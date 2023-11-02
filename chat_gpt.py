from flask import session
import openai
import os
import re

# Initialize OpenAI API key from environment variables
api_key = os.environ.get("OPENAI_API_KEY")

# Initialize the OpenAI API client
openai.api_key = api_key

def createFirstTimeUserChatGreeting(model="gpt-4", conversation_history=None, temperature=1, max_tokens=100):
    # Retrieve individual fields from the session
    # stage = session.get('stage', 'greeting')
    # user_intent = session.get('user_intent')
    # item_to_update = session.get('item_to_update')
    # quantity = session.get('quantity')
    # consumption_rate = session.get('consumption_rate')
    
    # print('Session state:', stage, user_intent, item_to_update, quantity, consumption_rate)

    # Initial greeting will depend on whether the user has already started a conversation
    # check database to see if user has started a conversation
    # if yes, then use the following prompt
    # content_message = "You are a helpful assistant specialized in managing grocery inventories. Respond as if you were greeting the user for the first time. "
    
    messages = [
        {
            "role": "system", 
            "content": "You are a helpful assistant specialized in managing grocery inventories. Respond as if you were greeting the user for the first time. "
        },
        {   
            "role": "user", 
            "content": "Greet me as this is the first time you are talking to me. You need to fnd out my consumption rate. "
        }
    ]
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature
    )
    
    generated_text = response['choices'][0]['message']['content'].strip()
    print('Generated text:', generated_text)
    return generated_text

def create_chat_completion(prompt, model="gpt-4", conversation_history=None, temperature=1, max_tokens=100):
    # Retrieve individual fields from the session
    stage = session.get('stage', 'greeting')
    user_intent = session.get('user_intent')
    item_to_update = session.get('item_to_update')
    quantity = session.get('quantity')
    consumption_rate = session.get('consumption_rate')
    
    print('Session state:', stage, user_intent, item_to_update, quantity, consumption_rate)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant specialized in managing grocery inventories."},
        {"role": "user", "content": prompt}  # Using prompt directly as it represents user's input
    ]
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature
    )
    
    generated_text = response['choices'][0]['message']['content'].strip()
    return generated_text

def parse_user_intent(user_input):
    """
    Parse the user's natural language input to determine the intent and parameters.
    
    Args:
        user_input (str): Natural language input from the user.
        
    Returns:
        dict: A dictionary containing the parsed intent and parameters.
    """
    user_input = user_input.lower().strip()  # Normalize the input to lowercase and remove leading/trailing whitespaces
    
    # Initialize an empty dictionary to hold the parsed information
    parsed_info = {
        'intent': None,
        'item': None,
        'quantity': None
    }
    
    # Identify intent and extract parameters
    if 'add' in user_input or 'create' in user_input:
        parsed_info['intent'] = 'create'
        parsed_info['item'] = re.search(r'add (.+?) to', user_input).group(1) if re.search(r'add (.+?) to', user_input) else None
        parsed_info['quantity'] = re.search(r'\b(\d+)\b', user_input).group(1) if re.search(r'\b(\d+)\b', user_input) else None
    elif 'remove' in user_input or 'delete' in user_input:
        parsed_info['intent'] = 'delete'
        parsed_info['item'] = re.search(r'remove (.+?) from', user_input).group(1) if re.search(r'remove (.+?) from', user_input) else None
    elif 'update' in user_input or 'change' in user_input:
        parsed_info['intent'] = 'update'
        parsed_info['item'] = re.search(r'update (.+?) to', user_input).group(1) if re.search(r'update (.+?) to', user_input) else None
        parsed_info['quantity'] = re.search(r'\b(\d+)\b', user_input).group(1) if re.search(r'\b(\d+)\b', user_input) else None
    elif 'show' in user_input or 'list' in user_input:
        parsed_info['intent'] = 'read'
    
    return parsed_info

def parse_gpt_response(gpt_response):
    # Initialize variables
    action = 'none'
    details = {}
    
    # Regular expressions for extracting item details
    item_name_re = re.compile(r'item name: (\w+)', re.IGNORECASE)
    item_quantity_re = re.compile(r'quantity: (\d+)', re.IGNORECASE)
    item_date_re = re.compile(r'last purchased: (\d{4}-\d{2}-\d{2})', re.IGNORECASE)
    
    # Logic to parse GPT's response and decide the CRUD operation
    if "added" in gpt_response.lower() or "create" in gpt_response.lower():
        action = 'create'
        details['name'] = item_name_re.search(gpt_response).group(1) if item_name_re.search(gpt_response) else None
        details['quantity'] = int(item_quantity_re.search(gpt_response).group(1)) if item_quantity_re.search(gpt_response) else None
        details['last_purchased'] = item_date_re.search(gpt_response).group(1) if item_date_re.search(gpt_response) else None
        
    elif "show" in gpt_response.lower() or "read" in gpt_response.lower():
        action = 'read'
        details['name'] = item_name_re.search(gpt_response).group(1) if item_name_re.search(gpt_response) else None
        
    elif "update" in gpt_response.lower():
        action = 'update'
        details['name'] = item_name_re.search(gpt_response).group(1) if item_name_re.search(gpt_response) else None
        details['quantity'] = int(item_quantity_re.search(gpt_response).group(1)) if item_quantity_re.search(gpt_response) else None
        details['last_purchased'] = item_date_re.search(gpt_response).group(1) if item_date_re.search(gpt_response) else None
        
    elif "remove" in gpt_response.lower() or "delete" in gpt_response.lower():
        action = 'delete'
        details['name'] = item_name_re.search(gpt_response).group(1) if item_name_re.search(gpt_response) else None
    
    return action, details

