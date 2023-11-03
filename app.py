from flask import Flask, request, render_template, redirect, url_for, flash, session
#from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from data import inventory
from database import db, create_pin, insert_pin_into_table, getPage
# from inventory_management import add_item, update_quantity, update_item, remove_item, calculate_consumption_rate
from inventory_management import add_item_to_inventory, get_item_details, update_item_details, delete_item_from_inventory
from chat_gpt import create_chat_completion, parse_user_intent, parse_gpt_response, createFirstTimeUserChatGreeting, gatherInformation
from conversation_state import ConversationState
from forms import PinForm
from models import UserState
import os

load_dotenv()  # Load environment variables from .env file

#db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(16).hex()
    # Setup database URI from the environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Silence the deprecation warning
    # app.config['DEBUG'] = True
    db.init_app(app)

    # Import models
    from models import InventoryItem, UserState
    migrate = Migrate(app, db)
    return app

app = create_app()

# render a template that allows the user to input an id so the app knows if the user is new or not?
@app.route('/', methods=['GET'])
def landing():
    form = PinForm()
    return render_template('landing.html', form=form)

@app.route('/process_pin', methods=['POST'])
def process_pin():
    form = PinForm()
    if form.validate_on_submit():
        pin = form.pin.data
        page = getPage(pin, UserState)
    return redirect(page)

@app.route('/create_pin', methods=['POST'])
def obtain_pin():
    if request.method == 'POST':
        pin = create_pin()
        insert_pin_into_table(pin, UserState)
    return redirect('/')

@app.route('/handle_input', methods=['POST'])
def handle_input():
    user_input = request.form['user_input']
    conversation_state = session.get('conversation_state')
    
    if conversation_state:
        conversation_state.update_last_user_response(user_input)
        prompt = conversation_state.get_context()
        response = create_chat_completion(prompt)
        conversation_state.update_last_gpt_response(response)
        
    return render_template('handle_input.html', gpt_response=response)

# @app.route('/natural_input', methods=['GET', 'POST'])
# def natural_input():
#     if request.method == 'POST':
#         user_input = request.form['user_input']
#         # Here, we'll call the ChatGPT function to interpret the user_input.
#         # Then, we'll process the ChatGPT response to update the inventory.
#         # Finally, we'll display the outcome to the user.
#         # This part will be implemented in the next steps.
#         return redirect('/natural_input')
#     return render_template('natural_input.html')

@app.route('/natural_input', methods=['GET', 'POST'])
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

@app.route('/first_time_user', methods=['GET', 'POST'])
def process_first_time_user():
    if request.method == 'GET':
        print('GET request')
        # user_input = request.form.get('user_input')
        # print(f"User Input: {user_input}")
        chat_gpt_response = createFirstTimeUserChatGreeting()
        session['chatgpt_response'] = chat_gpt_response
    if request.method == 'POST':
        print('POST request')
        user_input = request.form.get('user_input')
        chat_gpt_response = gatherInformation(user_input)
        session['chatgpt_response'] = chat_gpt_response
        
    return render_template('first_time_user.html')


if __name__ == "__main__":
    # app = create_app()
    app.run()



