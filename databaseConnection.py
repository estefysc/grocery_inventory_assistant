from flask_sqlalchemy import SQLAlchemy

class DatabaseConnection:
    _db_instance = None

    @classmethod
    def init_app(cls, app):
        if cls._db_instance is None:
            cls._db_instance = SQLAlchemy(app)
            print('Database instance created with app context')
        else:
            print('Database instance already exists')

    @classmethod
    def getDbInstance(cls):
        return cls._db_instance