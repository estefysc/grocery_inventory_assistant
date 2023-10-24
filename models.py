from app import db

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    last_purchased = db.Column(db.Date, nullable=False)
    consumption_rate = db.Column(db.Float, nullable=True)

class UserState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_time_user = db.Column(db.Boolean, default=True)
    purchase_frequency = db.Column(db.String(50), nullable=True)