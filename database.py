from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from random import randint

db = SQLAlchemy()

def create_pin():
    pin = randint(1000, 9999)
    print('Generated PIN: ' + str(pin))
    return pin

def insert_pin_into_table(pin):
    # Import is happening here to prevent "circular imports" error
    from models import UserState

    # Create a new UserState object with the given PIN
    new_user_state = UserState(id=pin, first_time_user=True)

    try:
        # Add to the database
        db.session.add(new_user_state)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        # TODO: add to logs
        print(str(e) + '\n' + 'Error inserting new user state into table')
        
    print('Successfully inserted new user state into table')

def checkIfFirstTimeUser(pin):++++
    # Check if the pin is in the database
    # If if is, check if this is a first time user


