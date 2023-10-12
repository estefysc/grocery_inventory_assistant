from flask import Flask, request, render_template, redirect, url_for, flash, session
#from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from data import inventory
from database import db
# from inventory_management import add_item, update_quantity, update_item, remove_item, calculate_consumption_rate
from inventory_management import add_item_to_inventory, get_item_details, update_item_details, delete_item_from_inventory
from chat_gpt import create_chat_completion, parse_user_intent, parse_gpt_response
from conversation_state import ConversationState
import os

load_dotenv()  # Load environment variables from .env file

#db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(16).hex()
    # Setup database URI from the environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Silence the deprecation warning
    db.init_app(app)

    # Import models
    from models import InventoryItem, UserState
    migrate = Migrate(app, db)
    return app

app = create_app()

@app.route('/start_conversation', methods=['GET', 'POST'])
def start_conversation():
    session['conversation_state'] = ConversationState()
    return render_template('start_conversation.html')

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

@app.route('/')
def home():
    return "Welcome to your Grocery Inventory Assistant!"

# @app.route('/home')
# def render_home():
#     return render_template('index.html', inventory=inventory)

# @app.route('/add_item', methods=['POST'])
# def form_add_item():
#     item_name = request.form['name']
#     item_quantity = int(request.form['quantity'])
#     item_last_purchased = request.form['last_purchased']
#     add_item(item_name, item_quantity, item_last_purchased)
#     return redirect('/home')

# @app.route('/update_item', methods=['POST'])
# def form_update_item():
#     item_name = request.form['name']
#     item_quantity = int(request.form['quantity'])
#     item_last_purchased = request.form['last_purchased']
#     update_item(item_name, item_quantity, item_last_purchased)
#     return redirect('/home')

# @app.route('/remove_item', methods=['POST'])
# def form_remove_item():
#     item_name = request.form['name']
#     remove_item(item_name)
#     return redirect('/home')

# @app.route('/inventory', methods=['GET'])
# def get_inventory():
#     return jsonify(inventory)

# @app.route('/inventory/add', methods=['POST'])
# def add_to_inventory():
#     item_data = request.json
#     add_item(item_data['name'], item_data['quantity'], item_data['last_purchased'])
#     return jsonify({"message": "Item added successfully!"})

# @app.route('/inventory/update', methods=['PUT'])
# def update_inventory_item():
#     item_data = request.json
#     update_item(item_data['name'], item_data['quantity'], item_data['last_purchased'])
#     return jsonify({"message": "Item updated successfully!"})

# @app.route('/inventory/remove', methods=['DELETE'])
# def remove_inventory_item():
#     item_name = request.json['name']
#     remove_item(item_name)
#     return jsonify({"message": f"Item {item_name} removed successfully!"})

# @app.route('/inventory/consumption-rate', methods=['GET'])
# def get_consumption_rate():
#     item_name = request.args.get('name')
#     rate = calculate_consumption_rate(item_name)
#     return jsonify({"consumption_rate": rate})

@app.route('/natural_input', methods=['GET', 'POST'])
def natural_input():
    if request.method == 'POST':
        user_input = request.form['user_input']
        # Here, we'll call the ChatGPT function to interpret the user_input.
        # Then, we'll process the ChatGPT response to update the inventory.
        # Finally, we'll display the outcome to the user.
        # This part will be implemented in the next steps.
        return redirect('/natural_input')
    return render_template('natural_input.html')

@app.route('/process_natural_input', methods=['POST'])
def process_natural_input():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        chat_gpt_response = create_chat_completion(user_input)
        
        # Parsing GPT's response to extract commands for CRUD operations
        action, details = parse_gpt_response(chat_gpt_response)
        
        if action == 'create':
            # Call the function to create a new inventory item
            add_item_to_inventory(details['name'], details['quantity'], details['last_purchased'])
            
        elif action == 'read':
            # Call the function to read details of an inventory item
            item_details = get_item_details(details['name'])
            # Pass item_details to the frontend, if needed
            flash(f"Item Details: {item_details}")
            
        elif action == 'update':
            # Call the function to update an existing inventory item
            update_item_details(details['name'], details['quantity'], details['last_purchased'])
            
        elif action == 'delete':
            # Call the function to delete an inventory item
            delete_item_from_inventory(details['name'])
        
        elif action == 'none':
            # No specific CRUD operation, maybe a query or other command
            flash(f"GPT Response: {chat_gpt_response}")
            
        return redirect(url_for('natural_input'))
        
    return render_template('natural_input.html')






if __name__ == "__main__":
    app.run(debug=True)



