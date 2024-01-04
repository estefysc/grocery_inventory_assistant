from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from assistants.inventoryAssistant import InventoryAssistant
from assistants.supervisor import Supervisor

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
    # Note: When you deal with HTTP requests in a web application, each request is independent. 
    # This means when a user first visits your page, a GET request is initiated, and the variables assistantId and thread are set within the scope of that request. 
    # However, once the response is sent back to the user, that instance of the function (along with its variables) essentially ceases to exist.
    # Later, when the user submits a form, triggering a POST request, a new instance of the process_first_time_user function is called. 
    # This new instance has its own set of variables. So, the assistantId and thread variables are re-initialized to None, and they don't retain the values they had during the GET request.
    
    print("process_first_time_user")

    userId = session['userId']
    assistanId, supervisorId = db.checkIfAgentsInSession(userId)
    assistantThreadId = db.getAssistantThreadIdFromSession(userId)
    supervisorThreadId = db.getSupervisorThreadIdFromSession(userId)
    
    if assistanId is None:
        print("No assistant found for this user.")
    else:
        print("Assistant found for this user.")

    assistant = InventoryAssistant("Grocery Inventory Assistant")
    supervisor = Supervisor("Grocery Inventory Supervisor")
    
    if request.method == 'GET':
        print("GET request - process_first_time_user")

        # print("(Development) Deleting all assistants..")
        # assistant.deleteAllAssistants()

        # Old API
        # chat_gpt_response = createFirstTimeUserChatGreeting()
        # session['chatgpt_response'] = chat_gpt_response
        
        assistantResponse = assistant.startFirstTimeUserInteraction(userId, db)
        session['chatgpt_response'] = assistantResponse
        
    if request.method == 'POST':
        print("POST request - process_first_time_user")
        user_input = request.form.get('user_input')

        # Old API
        # chat_gpt_response = gatherInformation(user_input)
        # session['chatgpt_response'] = chat_gpt_response

        assistantResponse = assistant.processFirstTimeUserInput(user_input, assistanId, assistantThreadId)
        session['chatgpt_response'] = assistantResponse

        if supervisorId is None:
            print("No supervisor found for this user.")
            supervisor.startInteraction(userId, db)
        else:
            print("Supervisor found for this user.")
            supervisorResponse = supervisor.analizeResponse(assistantResponse, supervisorId, supervisorThreadId)
            session['chatgpt_supervisor_response'] = supervisorResponse

    return render_template('first_time_user.html')