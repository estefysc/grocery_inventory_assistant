from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from databaseConnection import DatabaseConnection
from assistants.inventoryAssistant import InventoryAssistant
from assistants.supervisor import Supervisor
import os

load_dotenv()  # Load environment variables from .env file

def create_app():
    # Flask is designed to work with an application factory pattern, where a function like create_app sets up and returns a fully configured app instance. 
    # This design allows for better flexibility and testing.
    # Initializing components like DatabaseConnection, Migrate, and registering blueprints inside the create_app function ensures they are bound to the correct app context. 
    # It also ensures that these components are initialized every time create_app is called, which is essential for testing and other scenarios where you might create multiple app instances.
    
    app = Flask(__name__)
    app.secret_key = os.urandom(16).hex()
    # Setup database URI from the environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Silence the deprecation warning

    DatabaseConnection.init_app(app)
    db_conn = DatabaseConnection.getDbInstance()

    # Import models
    from models import InventoryItem, UserState
    migrate = Migrate(app, db_conn)

    # Import and register the Blueprint
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()



