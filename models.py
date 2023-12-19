# from app import db
from databaseConnection import DatabaseConnection
db_conn = DatabaseConnection.getDbInstance()

class InventoryItem(db_conn.Model):
    id = db_conn.Column(db_conn.Integer, primary_key=True)
    name = db_conn.Column(db_conn.String(50), nullable=False)
    quantity = db_conn.Column(db_conn.Integer, nullable=False)
    last_purchased = db_conn.Column(db_conn.Date, nullable=False)
    consumption_rate = db_conn.Column(db_conn.Float, nullable=True)

class UserState(db_conn.Model):
    id = db_conn.Column(db_conn.Integer, primary_key=True)
    first_time_user = db_conn.Column(db_conn.Boolean, default=True)
    purchase_frequency = db_conn.Column(db_conn.String(50), nullable=True)