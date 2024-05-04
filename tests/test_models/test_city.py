#!/usr/bin/python3
"""Test module for the City class"""
from tests.test_models.test_base_model import test_basemodel
from models.city import City
from models.place import Place
import sqlalchemy


class test_City(test_basemodel):
    """Test suite for City model"""

    def __init__(self, *args, **kwargs):
        """Initialize test suite"""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """Test if state_id is an attribute and is a string"""
        new = self.value()
        self.assertTrue(hasattr(new, 'state_id'))
        self.assertIsInstance(new.state_id, str)

    def test_name(self):
        """Test if name is an attribute and is a string"""
        new = self.value()
        self.assertTrue(hasattr(new, 'name'))
        self.assertIsInstance(new.name, str)

    def test_places_relationship(self):
        """Test the places relationship"""
        new = self.value()
        self.assertTrue(hasattr(new, 'places'))
        self.assertIsInstance(new.places, list)
        self.assertEqual(len(new.places), 0)

    def test_sqlalchemy_attributes(self):
        """Test attributes that are specific to SQLAlchemy"""
        new = self.value()
        self.assertTrue(hasattr(new, '__tablename__'))
        self.assertEqual(new.__tablename__, 'cities')
        self.assertTrue(isinstance(new.__mapper__.columns['name'], sqlalchemy.orm.attributes.InstrumentedAttribute))
        self.assertTrue(isinstance(new.__mapper__.columns['state_id'], sqlalchemy.orm.attributes.InstrumentedAttribute))
