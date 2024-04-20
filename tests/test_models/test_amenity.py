#!/usr/bin/python3
"""Test module for the Amenity class"""
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity
import sqlalchemy

class test_Amenity(test_basemodel):
    """Test suite for Amenity model"""

    def __init__(self, *args, **kwargs):
        """Initialize test suite"""
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name(self):
        """Test if name is an attribute and is a string"""
        new = self.value()
        self.assertTrue(hasattr(new, 'name'))
        self.assertIsInstance(new.name, str)
        self.assertFalse(getattr(new, 'name') is None)  # Ensures name is not None by default

    def test_sqlalchemy_attributes(self):
        """Test SQLAlchemy specific settings"""
        new = self.value()
        self.assertTrue(hasattr(new, '__tablename__'))
        self.assertEqual(new.__tablename__, 'amenities')
        self.assertTrue(isinstance(new.__mapper__.columns['name'], sqlalchemy.orm.attributes.InstrumentedAttribute))

    def test_place_amenities_relationship(self):
        """Test the relationship to Place through place_amenities"""
        new = self.value()
        self.assertTrue(hasattr(new, 'place_amenities'))
        self.assertEqual(len(new.place_amenities), 0)  # Should be empty list initially
