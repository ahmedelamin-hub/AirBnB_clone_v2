#!/usr/bin/python3
"""
City Module for HBNB project
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """
    The City class: represents the "cities" table in the database,
    with attributes 'id', 'name', and 'state_id' linking to the 'states' table.
    """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
