#!/usr/bin/python3
"""Test module for the Place class"""
from tests.test_models.test_base_model import test_basemodel
from models.place import Place
import sqlalchemy

class test_Place(test_basemodel):
    """Test suite for Place model"""

    def __init__(self, *args, **kwargs):
        """Initialize test suite"""
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_attributes_exist(self):
        """Test if all attributes exist"""
        new = self.value()
        attribute_list = [
            'city_id', 'user_id', 'name', 'description',
            'number_rooms', 'number_bathrooms', 'max_guest',
            'price_by_night', 'latitude', 'longitude', 'amenity_ids'
        ]
        for attribute in attribute_list:
            self.assertTrue(hasattr(new, attribute), f"Missing attribute: {attribute}")

    def test_attributes_type(self):
        """Test the type of each attribute"""
        new = self.value()
        self.assertIsInstance(new.city_id, str)
        self.assertIsInstance(new.user_id, str)
        self.assertIsInstance(new.name, str)
        self.assertIsInstance(new.description, str)
        self.assertIsInstance(new.number_rooms, int)
        self.assertIsInstance(new.number_bathrooms, int)
        self.assertIsInstance(new.max_guest, int)
        self.assertIsInstance(new.price_by_night, int)
        self.assertIsInstance(new.latitude, float)
        self.assertIsInstance(new.longitude, float)
        self.assertIsInstance(new.amenity_ids, list)

    def test_sqlalchemy_attributes(self):
        """Test SQLAlchemy specific settings"""
        new = self.value()
        self.assertTrue(hasattr(new, '__tablename__'))
        self.assertEqual(new.__tablename__, 'places')
        self.assertTrue(isinstance(new.__mapper__.columns['name'], sqlalchemy.orm.attributes.InstrumentedAttribute))

    def test_relationships_defined(self):
        """Test that relationships are correctly defined"""
        new = self.value()
        # Test for SQLAlchemy relationships (assuming back_populates are correctly set)
        self.assertTrue(hasattr(new, 'user'))
        self.assertTrue(hasattr(new, 'city'))
        self.assertTrue(hasattr(new, 'amenities'))  # This checks the relationship link

    def test_default_values(self):
        """Test default values for attributes that have defaults"""
        new = self.value()
        self.assertEqual(new.number_rooms, 0)
        self.assertEqual(new.number_bathrooms, 0)
        self.assertEqual(new.max_guest, 0)
        self.assertEqual(new.price_by_night, 0)
