#!/usr/bin/python3
"""Unit test module for User class."""
import unittest
from models.user import User
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

class test_User(unittest.TestCase):
    """Test suite for the User model."""

    @classmethod
    def setUpClass(cls):
        """Setup the class with session and engine."""
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.session = scoped_session(sessionmaker(bind=cls.engine, expire_on_commit=False))

    @classmethod
    def tearDownClass(cls):
        """Close session and drop database."""
        cls.session.remove()
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        """Create a new instance of User before each test."""
        self.user_instance = User(email="test@example.com", password="password", first_name="John", last_name="Doe")
        self.session.add(self.user_instance)
        self.session.commit()

    def tearDown(self):
        """Ensure each test does not affect others."""
        self.session.rollback()
        self.session.query(User).delete()
        self.session.commit()

    def test_email(self):
        """Test the email attribute."""
        self.assertEqual(self.user_instance.email, "test@example.com")
        self.assertIsInstance(self.user_instance.email, str)

    def test_password(self):
        """Test the password attribute."""
        self.assertEqual(self.user_instance.password, "password")
        self.assertIsInstance(self.user_instance.password, str)

    def test_first_name(self):
        """Test the first_name attribute."""
        self.assertEqual(self.user_instance.first_name, "John")
        self.assertIsInstance(self.user_instance.first_name, str)

    def test_last_name(self):
        """Test the last_name attribute."""
        self.assertEqual(self.user_instance.last_name, "Doe")
        self.assertIsInstance(self.user_instance.last_name, str)

    def test_relationships_places(self):
        """Test the User to Place relationship."""
        from models.place import Place
        place = Place(name="My place", user=self.user_instance)
        self.session.add(place)
        self.session.commit()
        self.assertIn(place, self.user_instance.places)

    def test_relationships_reviews(self):
        """Test the User to Review relationship."""
        from models.review import Review
        review = Review(text="Great!", user=self.user_instance)
        self.session.add(review)
        self.session.commit()
        self.assertIn(review, self.user_instance.reviews)

    def test_sqlalchemy_table(self):
        """Test if the SQLAlchemy table name is set correctly."""
        self.assertEqual(User.__tablename__, 'users')
