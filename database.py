from sqlalchemy.exc import SQLAlchemyError
from random import randint
from databaseConnection import DatabaseConnection
from flask import session

class Database:
    def __init__(self):
        self.db_conn = DatabaseConnection.getDbInstance()

    def create_pin(self):
        pin = randint(1000, 9999)
        print('Generated PIN: ' + str(pin))
        return pin

    def insert_pin_into_table(self, pin, UserState):
        # Create a new UserState object with the given PIN
        new_user_state = UserState(id=pin, first_time_user=True)

        try:
            # Add to the database
            self.db_conn.session.add(new_user_state)
            self.db_conn.session.commit()
        except SQLAlchemyError as e:
            self.db_conn.session.rollback()
            # TODO: add to logs
            print(str(e) + '\n' + 'Error inserting new user state into table')
            
        print('Successfully inserted new user state into table')

    def getPage(self, pin, UserState):
        redirect = None
        # Check if the pin is in the database
        pinExists = self.__checkIfPinExists(pin, UserState)
        if pinExists:
            print('Valid PIN')
            # TODO: for now, the pin will be used as user ID
            self.__createSessionObjects(pin)
            # Check if the user is a first time user
            isFirstTimeUser = self.__checkIfFirstTimeUser(pin, UserState)
            # TODO: Change the first_time_user column to False needs to be done once the user
            # has completed the onboarding process, not when they first enter the PIN.
            if isFirstTimeUser:
                # Change the first_time_user column to False
                self.__updateFirstTimeUser(pin, UserState)
                # return indication that the app should take the user to page to input beginning inventory
                redirect = '/first_time_user'
            else:
                redirect = '/natural_input'
        else:
            print('Invalid PIN')
            # TODO: figure out how to display error message to user if invalid PIN
            redirect = '/'
        return redirect
    
    def checkIfAgentsInSession(self, userId):
        assistantId = self.__checkIfAssistantExistsInSession(userId)
        supervisorId = self.__checkIfSupervisorExistsInSession(userId)
        return assistantId, supervisorId
    
    def getAssistantThreadIdFromSession(self, userId):
        threadId = None
        if 'originalAssistantThread' in session and userId in session['originalAssistantThread']:
            threadId = session['originalAssistantThread'][userId]
        return threadId
    
    def getSupervisorThreadIdFromSession(self, userId):
        threadId = None
        if 'originalSupervisorThread' in session and userId in session['originalSupervisorThread']:
            threadId = session['originalSupervisorThread'][userId]
        return threadId
    
    def __createSessionObjects(self, userId):
        self.__createAgentsSessionObjects()
        self.__checkUserIdInSession(userId)
        self.__createThreadSessionObjects()

    def addAssistantIdToSession(self, userId, assistantId):
        session['assistants'][userId] = assistantId

    def addSupervisorIdToSession(self, userId, supervisorId):
        session['supervisors'][userId] = supervisorId

    def addOriginalAssistantThreadIdToSession(self, userId, threadId):
        session['originalAssistantThread'][userId] = threadId

    def addOriginalSupervisorThreadIdToSession(self, userId, threadId):
        session['originalSupervisorThread'][userId] = threadId

    def get_database_info(self):
        """Return a list of dicts containing the table name and columns for each table in the database."""
        table_dicts = []

        for table_name in self.__get_table_names():
            columns_names = self.__get_column_names(table_name)
            table_dicts.append({"table_name": table_name, "column_names": columns_names})
            
        return table_dicts
    
    def __createAgentsSessionObjects(self):
        if 'assistants' not in session:
            print("Assistants not in session. Creating object..")
            session['assistants'] = {}
        else:
            print("Assistants already in session.")

        if 'suppervisors' not in session:
            print("Supervisors not in session. Creating object..")
            session['supervisors'] = {}
        else:
            print("Supervisors already in session.")

    def __createThreadSessionObjects(self):
        if 'originalAssistantThread' not in session:
            print("originalAssistantThread not in session. Creating object..")
            session['originalAssistantThread'] = {}
        else:
            print("originalAssistantThread already in session.")

        if 'originalSupervisorThread' not in session:
            print("originalSupervisorThread not in session. Creating object..")
            session['originalSupervisorThread'] = {}
        else:
            print("originalSupervisorThread already in session.")
    
    def __checkIfAssistantExistsInSession(self, userId):
        assistantId = None
        if 'assistants' in session and userId in session['assistants']:
            assistantId = session['assistants'][userId]
        return assistantId
    
    def __checkIfSupervisorExistsInSession(self, userId):
        supervisorId = None
        if 'supervisors' in session and userId in session['supervisors']:
            supervisorId = session['supervisors'][userId]
        return supervisorId

    def __checkIfPinExists(self, pin, UserState):
        pinExists = self.db_conn.session.query(UserState.query.filter_by(id=pin).exists()).scalar()
        print('Does the pin exist? ' + str(pinExists))
        return pinExists

    def __checkIfFirstTimeUser(self, pin, UserState):
        # Query the UserState table for the specific PIN
        user_state = UserState.query.filter_by(id=pin).first()
        isFirstTimeUser = user_state.first_time_user
        print(isFirstTimeUser)
        return isFirstTimeUser

    def __updateFirstTimeUser(self, pin, UserState):
        userState = UserState.query.filter_by(id=pin).first()
        userState.first_time_user = False
        try:
            self.db_conn.session.commit()
            print('Successfully updated first_time_user value to False')
        except SQLAlchemyError as e:
            print(str(e) + '\n' + 'Error updating first_time_user value to False')
            self.db_conn.session.rollback()

    def __get_table_names(self):
        """Return a list of table names."""
        table_names = []
        metadata = self.db_conn.MetaData()
        metadata.reflect(bind=self.db_conn.engine)

        for table in metadata.tables:
            table_names.append(table)

        return table_names

    def __get_column_names(self, table_name):
        """Return a list of column names."""
        column_names = []
        metadata = self.db_conn.MetaData()
        metadata.reflect(bind=self.db_conn.engine)
        table = metadata.tables.get(table_name)

        for column in table.columns:
            column_names.append(column.name)

        return column_names
    
    def __checkUserIdInSession(self, userId):
        if 'userId' not in session:
            print("Adding user to session")
            session['userId'] = str(userId)
            session.modified = True
        else:
            print("User already in session")

# ------ Module code

# from sqlalchemy.exc import SQLAlchemyError
# from random import randint
# import databaseConnection
# from flask import session

# db_conn = databaseConnection.get_db_instance()

# def create_pin():
#     pin = randint(1000, 9999)
#     print('Generated PIN: ' + str(pin))
#     return pin

# def insert_pin_into_table(pin, UserState):
#     new_user_state = UserState(id=pin, first_time_user=True)
#     try:
#         db_conn.session.add(new_user_state)
#         db_conn.session.commit()
#     except SQLAlchemyError as e:
#         db_conn.session.rollback()
#         print(str(e) + '\n' + 'Error inserting new user state into table')
#     print('Successfully inserted new user state into table')

# def getPage(pin, UserState):
#     redirect = None
#     pinExists = _checkIfPinExists(pin, UserState)
#     if pinExists:
#         print('Valid PIN')
#         _createSessionObjects(pin)
#         isFirstTimeUser = _checkIfFirstTimeUser(pin, UserState)
#         if isFirstTimeUser:
#             _updateFirstTimeUser(pin, UserState)
#             redirect = '/first_time_user'
#         else:
#             redirect = '/natural_input'
#     else:
#         print('Invalid PIN')
#         redirect = '/'
#     return redirect

# def checkIfAgentsInSession(userId):
#     assistantId = _checkIfAssistantExistsInSession(userId)
#     supervisorId = _checkIfSupervisorExistsInSession(userId)
#     return assistantId, supervisorId

# def getAssistantThreadIdFromSession(userId):
#     threadId = None
#     if 'originalAssistantThread' in session and userId in session['originalAssistantThread']:
#         threadId = session['originalAssistantThread'][userId]
#     return threadId

# def getSupervisorThreadIdFromSession(userId):
#     threadId = None
#     if 'originalSupervisorThread' in session and userId in session['originalSupervisorThread']:
#         threadId = session['originalSupervisorThread'][userId]
#     return threadId

# def addAssistantIdToSession(userId, assistantId):
#     session['assistants'][userId] = assistantId

# def addSupervisorIdToSession(userId, supervisorId):
#     session['supervisors'][userId] = supervisorId

# def addOriginalAssistantThreadIdToSession(userId, threadId):
#     session['originalAssistantThread'][userId] = threadId

# def addOriginalSupervisorThreadIdToSession(userId, threadId):
#     session['originalSupervisorThread'][userId] = threadId

# def get_database_info():
#     table_dicts = []
#     for table_name in _get_table_names():
#         columns_names = _get_column_names(table_name)
#         table_dicts.append({"table_name": table_name, "column_names": columns_names})
#     return table_dicts

# # Private functions

# def _createSessionObjects(userId):
#     _createAgentsSessionObjects()
#     _checkUserIdInSession(userId)
#     _createThreadSessionObjects()

# def _createAgentsSessionObjects():
#     if 'assistants' not in session:
#         print("Assistants not in session. Creating object..")
#         session['assistants'] = {}
#     else:
#         print("Assistants already in session.")

#     if 'suppervisors' not in session:
#         print("Supervisors not in session. Creating object..")
#         session['supervisors'] = {}
#     else:
#         print("Supervisors already in session.")

# def _createThreadSessionObjects():
#     if 'originalAssistantThread' not in session:
#         print("originalAssistantThread not in session. Creating object..")
#         session['originalAssistantThread'] = {}
#     else:
#         print("originalAssistantThread already in session.")

#     if 'originalSupervisorThread' not in session:
#         print("originalSupervisorThread not in session. Creating object..")
#         session['originalSupervisorThread'] = {}
#     else:
#         print("originalSupervisorThread already in session.")

# def _checkIfAssistantExistsInSession(userId):
#     assistantId = None
#     if 'assistants' in session and userId in session['assistants']:
#         assistantId = session['assistants'][userId]
#     return assistantId

# def _checkIfSupervisorExistsInSession(userId):
#     supervisorId = None
#     if 'supervisors' in session and userId in session['supervisors']:
#         supervisorId = session['supervisors'][userId]
#     return supervisorId

# def _checkIfPinExists(pin, UserState):
#     pinExists = db_conn.session.query(UserState.query.filter_by(id=pin).exists()).scalar()
#     print('Does the pin exist? ' + str(pinExists))
#     return pinExists

# def _checkIfFirstTimeUser(pin, UserState):
#     user_state = UserState.query.filter_by(id=pin).first()
#     isFirstTimeUser = user_state.first_time_user
#     print(isFirstTimeUser)
#     return isFirstTimeUser

# def _updateFirstTimeUser(pin, UserState):
#     userState = UserState.query.filter_by(id=pin).first()
#     userState.first_time_user = False
#     try:
#         db_conn.session.commit()
#         print('Successfully updated first_time_user value to False')
#     except SQLAlchemyError as e:
#         print(str(e) + '\n' + 'Error updating first_time_user value to False')
#         db_conn.session.rollback()

# def _get_table_names():
#     table_names = []
#     metadata = db_conn.MetaData()
#     metadata.reflect(bind=db_conn.engine)
#     for table in metadata.tables:
#         table_names.append(table)
#     return table_names

# def _get_column_names(table_name):
#     column_names = []
#     metadata = db_conn.MetaData()
#     metadata.reflect(bind=db_conn.engine)
#     table = metadata.tables.get(table_name)
#     for column in table.columns:
#         column_names.append(column.name)
#     return column_names

# def _checkUserIdInSession(userId):
#     # This function was not defined in the original class, but it's called in _createSessionObjects
#     # You may want to implement it based on your requirements
#     pass
    



