#!/usr/bin/python3
"""
State Module for HBNB project
"""
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models

class State(BaseModel, Base):
    """
    The State class: represents the "states" table in the database,
    with the attribute 'name' and a relationship to the 'cities' table.
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        # For DBStorage: setup relationship to City
        cities = relationship("City", backref="state", cascade="all, delete-orphan")
    else:
        # For FileStorage: a property to return list of City instances with state_id equals to this State's id
        @property
        def cities(self):
            """Return the list of City instances with state_id equals to this State's id."""
            from models.city import City
            city_list = models.storage.all(City).values()
            return [city for city in city_list if city.state_id == self.id]
