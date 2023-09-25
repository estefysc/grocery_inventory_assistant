from datetime import datetime
from data import inventory

def update_quantity(item_name, new_quantity):
    old_quantity = inventory[item_name]['quantity']
    last_purchased_date = datetime.strptime(inventory[item_name]['last_purchased_date'], '%Y-%m-%d')
    days_since_last_purchase = (datetime.now() - last_purchased_date).days
    
    # Update the item details
    inventory[item_name]['quantity'] = new_quantity
    inventory[item_name]['last_purchased_date'] = datetime.now().strftime('%Y-%m-%d')
    
    # Calculate and update the consumption rate
    if days_since_last_purchase > 0:  # Avoid division by zero
        consumption_rate = (old_quantity - new_quantity) / days_since_last_purchase
        inventory[item_name]['consumption_rate'] = consumption_rate

def add_item(item_name, quantity, last_purchased_date):
    inventory[item_name] = {
        'quantity': quantity,
        'last_purchased_date': last_purchased_date,
        'consumption_rate': None  # Initialized to None, will be calculated later
    }

def calculate_consumption_rate(item_name):
    last_purchased_date = datetime.strptime(inventory[item_name]['last_purchased_date'], '%Y-%m-%d')
    days_since_last_purchase = (datetime.now() - last_purchased_date).days
    current_quantity = inventory[item_name]['quantity']
    
    if days_since_last_purchase > 0:  # Avoid division by zero
        return (inventory[item_name]['last_quantity'] - current_quantity) / days_since_last_purchase
    
def update_item(name, new_quantity, new_last_purchased):
    global inventory
    if name in inventory:
        inventory[name]['quantity'] = new_quantity
        inventory[name]['last_purchased'] = new_last_purchased
    else:
        print(f"Item {name} not found in inventory.")

def remove_item(name):
    global inventory
    if name in inventory:
        del inventory[name]
    else:
        print(f"Item {name} not found in inventory.")
