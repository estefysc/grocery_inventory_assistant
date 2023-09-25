from flask import Flask, jsonify, request, render_template, redirect, session
from data import inventory
from inventory_management import add_item, update_quantity, update_item, remove_item, calculate_consumption_rate
from chat_gpt import create_chat_completion
import os

app = Flask(__name__)
# Using os.urandom(16).hex() will generate a new random key each time your app starts. This is often sufficient for development and testing.
# However, for a production environment, you would generally set a consistent secret key, so that server restarts don't invalidate existing user sessions. 
# This is usually done by setting an environment variable, as previously described.
app.secret_key = os.urandom(16).hex()

@app.route('/')
def home():
    return "Welcome to your Grocery Inventory Assistant!"

@app.route('/home')
def render_home():
    return render_template('index.html', inventory=inventory)

@app.route('/add_item', methods=['POST'])
def form_add_item():
    item_name = request.form['name']
    item_quantity = int(request.form['quantity'])
    item_last_purchased = request.form['last_purchased']
    add_item(item_name, item_quantity, item_last_purchased)
    return redirect('/home')

@app.route('/update_item', methods=['POST'])
def form_update_item():
    item_name = request.form['name']
    item_quantity = int(request.form['quantity'])
    item_last_purchased = request.form['last_purchased']
    update_item(item_name, item_quantity, item_last_purchased)
    return redirect('/home')

@app.route('/remove_item', methods=['POST'])
def form_remove_item():
    item_name = request.form['name']
    remove_item(item_name)
    return redirect('/home')

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory)

@app.route('/inventory/add', methods=['POST'])
def add_to_inventory():
    item_data = request.json
    add_item(item_data['name'], item_data['quantity'], item_data['last_purchased'])
    return jsonify({"message": "Item added successfully!"})

@app.route('/inventory/update', methods=['PUT'])
def update_inventory_item():
    item_data = request.json
    update_item(item_data['name'], item_data['quantity'], item_data['last_purchased'])
    return jsonify({"message": "Item updated successfully!"})

@app.route('/inventory/remove', methods=['DELETE'])
def remove_inventory_item():
    item_name = request.json['name']
    remove_item(item_name)
    return jsonify({"message": f"Item {item_name} removed successfully!"})

@app.route('/inventory/consumption-rate', methods=['GET'])
def get_consumption_rate():
    item_name = request.args.get('name')
    rate = calculate_consumption_rate(item_name)
    return jsonify({"consumption_rate": rate})

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
    user_input = request.form['user_input']

    # Print user input for debugging
    print("User Input:", user_input)
    
    # Interpret the user's natural language input using ChatGPT
    interpreted_response = create_chat_completion(user_input)

    # Print ChatGPT response for debugging
    print("ChatGPT Response:", interpreted_response)

    # Store the ChatGPT response in a session variable
    session['chatgpt_response'] = interpreted_response
    
    # Simplified parsing logic (this could get quite complex depending on what you're doing)
    # if "bananas" in interpreted_response and "two" in interpreted_response:
    #     update_quantity("Bananas", 2)  # Update the quantity of Bananas to 2 in the inventory
    
    return redirect('/natural_input')  # Redirect back to the form page

# You can add more routes to remove, update, and get specific items

if __name__ == "__main__":
    app.run(debug=True)



