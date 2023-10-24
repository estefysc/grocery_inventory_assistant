from app import db, create_app
from models import InventoryItem  # Importing the model you defined

app = create_app()

with app.app_context():
    db.create_all()

print("Database tables created.")