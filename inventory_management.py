from database import db
from models import InventoryItem

def add_item_to_inventory(item_name, quantity, last_purchased, consumption_rate=None):
    new_item = InventoryItem(
        name=item_name,
        quantity=quantity,
        last_purchased=last_purchased,
        consumption_rate=consumption_rate
    )
    db.session.add(new_item)
    db.session.commit()
    return f"Added {item_name} to the inventory."

def get_item_details(item_name):
    item = InventoryItem.query.filter_by(name=item_name).first()
    if item:
        return f"{item.name}: Quantity = {item.quantity}, Last Purchased = {item.last_purchased}, Consumption Rate = {item.consumption_rate}"
    else:
        return f"Item {item_name} not found in inventory."

def update_item_details(item_name, new_quantity, new_last_purchased, new_consumption_rate=None):
    item = InventoryItem.query.filter_by(name=item_name).first()
    if item:
        item.quantity = new_quantity
        item.last_purchased = new_last_purchased
        if new_consumption_rate:
            item.consumption_rate = new_consumption_rate
        db.session.commit()
        return f"Updated details for {item_name}."
    else:
        return f"Item {item_name} not found in inventory."

def delete_item_from_inventory(item_name):
    item = InventoryItem.query.filter_by(name=item_name).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return f"Deleted {item_name} from inventory."
    else:
        return f"Item {item_name} not found in inventory."
