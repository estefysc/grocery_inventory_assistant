from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from random import randint

# Note: Dependency injection is done in some of the functions to prevent the circular import error

db = SQLAlchemy()

def create_pin():
    pin = randint(1000, 9999)
    print('Generated PIN: ' + str(pin))
    return pin

def insert_pin_into_table(pin, UserState):
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

def allowSignIn(pin, UserState):
    # Check if the pin is in the database
    validPin = __checkIfPinExists(pin, UserState)
    
    if validPin:
        __checkIfFirstTimeUser(pin, UserState)
        # if first time user, take them to one page
        # if not first time user, take them to another page
    else:
        # do not allow sign in
        print('Invalid PIN')

def __checkIfPinExists(pin, UserState):
    pinExists = db.session.query(UserState.query.filter_by(id=pin).exists()).scalar()
    print('Does the pin exist? ' + str(pinExists))
    return pinExists

def __checkIfFirstTimeUser(pin, UserState):
    # Query the UserState table for the specific PIN
    user_state = UserState.query.filter_by(id=pin).first()
    isFirstTimeUser = user_state.first_time_user
    print(isFirstTimeUser)
    return isFirstTimeUser
    


