#!/usr/bin/python3
"""Test module for the Review class."""
import unittest
from models.review import Review
from models.base_model import Base, BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

class test_review(unittest.TestCase):
    """Test suite for the Review model."""

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
        """Create a new instance of Review before each test."""
        self.session.expire_on_commit = False
        self.review = Review(text="Great place!", place_id="12345", user_id="67890")
        self.session.add(self.review)
        self.session.commit()

    def tearDown(self):
        """Rollback session after each test."""
        self.session.rollback()
        self.session.query(Review).delete()
        self.session.commit()

    def test_attributes_exist(self):
        """Test if all required attributes exist."""
        self.assertTrue(hasattr(self.review, 'text'))
        self.assertTrue(hasattr(self.review, 'place_id'))
        self.assertTrue(hasattr(self.review, 'user_id'))

    def test_attributes_type(self):
        """Test the type of each attribute."""
        self.assertIsInstance(self.review.text, str)
        self.assertIsInstance(self.review.place_id, str)
        self.assertIsInstance(self.review.user_id, str)

    def test_sqlalchemy_table(self):
        """Test SQLAlchemy table configuration."""
        self.assertEqual(Review.__tablename__, 'reviews')

    def test_relationships(self):
        """Test ORM relationships."""
        self.assertIsNotNone(self.review.user)
        self.assertIsNotNone(self.review.place)

    def test_foreign_key_constraints(self):
        """Test foreign key constraints."""
        review = Review(text="Another review", place_id="invalid", user_id="invalid")
        self.session.add(review)
        with self.assertRaises(Exception):
            self.session.commit()  # This should raise an exception due to FK constraints

    def test_review_str_representation(self):
        """Test the custom string representation."""
        expected_str = '[Review] ({}) {}'.format(self.review.id, self.review.__dict__)
        self.assertEqual(str(self.review), expected_str)
