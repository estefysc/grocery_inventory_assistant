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

def getPage(pin, UserState):
    redirect = None
    # Check if the pin is in the database
    pinExists = __checkIfPinExists(pin, UserState)
    if pinExists:
        # Check if the user is a first time user
        isFirstTimeUser = __checkIfFirstTimeUser(pin, UserState)
        if isFirstTimeUser:
            # Change the first_time_user column to False
            __updateFirstTimeUser(pin, UserState)
            # return indication that the app should take the user to page to input beginning inventory
            redirect = '/first_time_user'
        else:
            redirect = '/natural_input'
    else:
        print('Invalid PIN')
        # TODO: figure out how to display error message to user if invalid PIN
        redirect = '/'
    return redirect

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

def __updateFirstTimeUser(pin, UserState):
    userState = UserState.query.filter_by(id=pin).first()
    userState.firstTimeUser = False
    try:
        db.session.commit()
        print('Successfully updated first time user')
    except SQLAlchemyError as e:
        print(str(e) + '\n' + 'Error updating first time user')
        db.session.rollback()


