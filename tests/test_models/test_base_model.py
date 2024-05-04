#!/usr/bin/python3
"""Unit test module for BaseModel class."""
import unittest
from models.base_model import BaseModel
from datetime import datetime
from uuid import UUID
import json
import os
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

class test_basemodel(unittest.TestCase):
    """Test suite for testing the BaseModel class."""

    @classmethod
    def setUpClass(cls):
        """Set up for test."""
        cls.engine = create_engine('sqlite:///:memory:')
        BaseModel.metadata.create_all(cls.engine)
        cls.session = scoped_session(sessionmaker(bind=cls.engine))

    @classmethod
    def tearDownClass(cls):
        """Final cleanup."""
        cls.session.remove()
        BaseModel.metadata.drop_all(cls.engine)

    def setUp(self):
        """Set up test methods."""
        self.session.expire_on_commit = False
        self.base_instance = BaseModel()
        self.session.add(self.base_instance)
        self.session.commit()

    def tearDown(self):
        """Clean up test methods."""
        self.session.rollback()
        self.session.query(BaseModel).delete()
        self.session.commit()

    def test_instance_creation(self):
        """Test instantiation of BaseModel object."""
        self.assertTrue(hasattr(self.base_instance, 'id'))
        self.assertTrue(hasattr(self.base_instance, 'created_at'))
        self.assertTrue(hasattr(self.base_instance, 'updated_at'))

    def test_id(self):
        """Test the type of id."""
        self.assertIsInstance(self.base_instance.id, str)

    def test_created_at(self):
        """Test the type of created_at."""
        self.assertIsInstance(self.base_instance.created_at, datetime)

    def test_updated_at(self):
        """Test the type of updated_at."""
        self.assertIsInstance(self.base_instance.updated_at, datetime)

    def test_str_representation(self):
        """Test the str method of BaseModel."""
        expected = '[BaseModel] ({}) {}'.format(self.base_instance.id, self.base_instance.__dict__)
        self.assertEqual(str(self.base_instance), expected)

    def test_save(self):
        """Test the save method updates `updated_at`."""
        old_updated_at = self.base_instance.updated_at
        self.base_instance.save()
        self.session.commit()
        self.assertNotEqual(old_updated_at, self.base_instance.updated_at)

    def test_to_dict(self):
        """Test to_dict method."""
        base_dict = self.base_instance.to_dict()
        self.assertIsInstance(base_dict, dict)
        self.assertIn('created_at', base_dict)
        self.assertIn('updated_at', base_dict)

    def test_delete(self):
        """Test delete method."""
        base_id = self.base_instance.id
        self.base_instance.delete()
        self.session.commit()
        self.assertIsNone(self.session.get(BaseModel, base_id))
