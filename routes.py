from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from assistant_functionality import Assistant 

# Create a Blueprint
main = Blueprint('main', __name__)


from chat_gpt import create_chat_completion, parse_user_intent, parse_gpt_response, createFirstTimeUserChatGreeting, gatherInformation
from conversation_state import ConversationState
from forms import PinForm

from models import InventoryItem, UserState

from database import Database
db = Database()

# Define routes using the Blueprint
@main.route('/', methods=['GET'])
def landing():
    form = PinForm()
    return render_template('landing.html', form=form)

@main.route('/process_pin', methods=['POST'])
def process_pin():
    form = PinForm()
    if form.validate_on_submit():
        pin = form.pin.data
        page = db.getPage(pin, UserState)
    return redirect(page)

@main.route('/create_pin', methods=['POST'])
def obtain_pin():
    if request.method == 'POST':
        pin = db.create_pin()
        db.insert_pin_into_table(pin, UserState)
    return redirect('/')

@main.route('/handle_input', methods=['POST'])
def handle_input():
    user_input = request.form['user_input']
    conversation_state = session.get('conversation_state')
    
    if conversation_state:
        conversation_state.update_last_user_response(user_input)
        prompt = conversation_state.get_context()
        response = create_chat_completion(prompt)
        conversation_state.update_last_gpt_response(response)
        
    return render_template('handle_input.html', gpt_response=response)

# @main.route('/natural_input', methods=['GET', 'POST'])
# def natural_input():
#     if request.method == 'POST':
#         user_input = request.form['user_input']
#         # Here, we'll call the ChatGPT function to interpret the user_input.
#         # Then, we'll process the ChatGPT response to update the inventory.
#         # Finally, we'll display the outcome to the user.
#         # This part will be implemented in the next steps.
#         return redirect('/natural_input')
#     return render_template('natural_input.html')

@main.route('/natural_input', methods=['GET', 'POST'])
def process_natural_input():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        print(f"User Input: {user_input}")
        chat_gpt_response = create_chat_completion(user_input)
        print(f"GPT Response: {chat_gpt_response}")
        session['chatgpt_response'] = chat_gpt_response
        # Parsing GPT's response to extract commands for CRUD operations
        # action, details = parse_gpt_response(chat_gpt_response)
        
        # if action == 'create':
        #     # Call the function to create a new inventory item
        #     add_item_to_inventory(details['name'], details['quantity'], details['last_purchased'])
            
        # elif action == 'read':
        #     # Call the function to read details of an inventory item
        #     item_details = get_item_details(details['name'])
        #     # Pass item_details to the frontend, if needed
        #     flash(f"Item Details: {item_details}")
            
        # elif action == 'update':
        #     # Call the function to update an existing inventory item
        #     update_item_details(details['name'], details['quantity'], details['last_purchased'])
            
        # elif action == 'delete':
        #     # Call the function to delete an inventory item
        #     delete_item_from_inventory(details['name'])
        
        # elif action == 'none':
        #     # No specific CRUD operation, maybe a query or other command
        #     flash(f"GPT Response: {chat_gpt_response}")
            
        # return redirect(url_for('natural_input'))
    return render_template('natural_input.html')

@main.route('/first_time_user', methods=['GET', 'POST'])
def process_first_time_user():
    assistant = Assistant("Grocery Inventory Assistant")
    assistantId = None
    thread = None

    if request.method == 'GET':
        # chat_gpt_response = createFirstTimeUserChatGreeting()
        # session['chatgpt_response'] = chat_gpt_response

        assistantId, thread, session['chatgpt_response'] = assistant.startFirstTimeUserInteraction()
        
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        # chat_gpt_response = gatherInformation(user_input)
        # session['chatgpt_response'] = chat_gpt_response

        session['chatgpt_response'] = assistant.processFirstTimeUserInput(user_input, assistantId, thread)

        
    return render_template('first_time_user.html')