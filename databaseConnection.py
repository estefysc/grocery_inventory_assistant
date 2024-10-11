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

# from flask_sqlalchemy import SQLAlchemy

# _db_instance = None

# def init_app(app):
#     global _db_instance
#     if _db_instance is None:
#         _db_instance = SQLAlchemy(app)
#         print('Database instance created with app context')
#     else:
#         print('Database instance already exists')

# def get_db_instance():
#     return _db_instance