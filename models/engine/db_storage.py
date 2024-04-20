#!/usr/bin/python3
"""
DBStorage Module for HBNB project
"""

from os import getenv
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import Base


class DBStorage:
    """Database Storage class handling long-term storage of HBNB entities"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage instance"""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST', 'localhost')
        db = getenv('HBNB_MYSQL_DB')
        environment = getenv('HBNB_ENV')

        # Create the engine
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{db}', pool_pre_ping=True)

        # Drop all tables if environment is set to 'test'
        if environment == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects of a certain type from the database"""
        obj_dict = {}
        if cls:
            objects = self.__session.query(cls).all()
            for obj in objects:
                key = f'{obj.__class__.__name__}.{obj.id}'
                obj_dict[key] = obj
        else:
            from models import classes
            for class_name in classes:
                objects = self.__session.query(classes[class_name]).all()
                for obj in objects:
                    key = f'{class_name}.{obj.id}'
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        ScopedSession = scoped_session(session_factory)
        self.__session = ScopedSession()

# Be sure to close the session properly if needed:
    def close(self):
        """Close the current session"""
        self.__session.close()
