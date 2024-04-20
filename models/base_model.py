#!/usr/bin/python3
"""
This module defines a base class for all models in our hbnb clone
using SQLAlchemy.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime
import uuid


# Base declaration for SQLAlchemy
Base = declarative_base()


class BaseModel:
    """
    A base class for all hbnb models that provides common attributes
    and methods for other classes and doesn't inherit directly from Base.
    """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Initializes a new model instance. If `kwargs` are provided,
        it sets attributes according to key-value pairs, handling
        specific keys for datetime fields.
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()
        else:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                setattr(self, key, value)
        
        from models import storage
        storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the instance. This method
        formats the class name, ID, and dictionary of attributes for clearer readability.
        """
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """
        Saves the instance to the database and updates 'updated_at'
        with the current datetime.
        """
        self.updated_at = datetime.utcnow()
        from models import storage
        storage.save(self)

    def delete(self):
        """
        Deletes the instance from the database via the storage handler.
        """
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """
        Returns a dictionary representation of the instance.
        This includes all key-values of the instance's __dict__,
        with adjustments for SQLAlchemy and converts datetime objects
        to ISO format strings.
        """
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop('_sa_instance_state', None)  # Remove instance state
        return dictionary
