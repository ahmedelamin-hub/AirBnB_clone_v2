#!/usr/bin/python3
"""Unit test module for State class."""
import unittest
from models.state import State
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models import storage_type

class test_state(unittest.TestCase):
    """Test suite for State model."""

    @classmethod
    def setUpClass(cls):
        """Set up for test by creating database engine and session."""
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.session = scoped_session(sessionmaker(bind=cls.engine, expire_on_commit=False))

    @classmethod
    def tearDownClass(cls):
        """Tear down test by closing session and dropping the database."""
        cls.session.remove()
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        """Begin each test with a new State object."""
        self.state_instance = State(name="California")
        self.session.add(self.state_instance)
        self.session.commit()

    def tearDown(self):
        """Ensure each test does not affect others."""
        self.session.rollback()
        self.session.query(State).delete()
        self.session.commit()

    def test_name_attribute(self):
        """Test the name attribute of State."""
        self.assertEqual(self.state_instance.name, "California")
        self.assertIsInstance(self.state_instance.name, str)

    def test_sqlalchemy_table(self):
        """Test if the SQLAlchemy table name is set correctly."""
        self.assertEqual(State.__tablename__, 'states')

    def test_relationships(self):
        """Test the relationships in SQLAlchemy mode."""
        if storage_type == 'db':
            from models.city import City
            city = City(name="San Francisco", state=self.state_instance)
            self.session.add(city)
            self.session.commit()
            self.assertIn(city, self.state_instance.cities)
        else:
            self.assertTrue(hasattr(self.state_instance, 'cities'))

    def test_cities_method(self):
        """Test the FileStorage cities method if it correctly lists City instances."""
        if storage_type != 'db':
            from models.city import City
            city = City(name="San Francisco", state_id=self.state_instance.id)
            storage.new(city)
            city_list = self.state_instance.cities
            self.assertIn(city, city_list)

    def test_to_dict(self):
        """Test conversion to dictionary."""
        state_dict = self.state_instance.to_dict()
        self.assertEqual(state_dict['name'], 'California')
        self.assertTrue('created_at' in state_dict)
        self.assertTrue('updated_at' in state_dict)
