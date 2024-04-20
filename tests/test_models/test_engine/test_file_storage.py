#!/usr/bin/python3
"""Module for testing file storage"""
import unittest
import os
import json
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City
from models.amenity import Amenity

class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    @classmethod
    def setUpClass(cls):
        """Set up for the class"""
        cls.user = User(email="test@example.com", password="test", first_name="Test", last_name="Example")
        cls.storage = storage
        cls.file_path = storage._FileStorage__file_path

    @classmethod
    def tearDownClass(cls):
        """Clean up files and objects after tests"""
        try:
            os.remove(cls.file_path)
        except FileNotFoundError:
            pass

    def setUp(self):
        """Clear storage before each test"""
        type(self.storage)._FileStorage__objects = {}

    def tearDown(self):
        """Remove storage file after each test"""
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass

    def test_all_return_type(self):
        """Test that all() returns a dict"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_all_with_class(self):
        """Test all with class filter"""
        self.storage.new(self.user)
        self.storage.save()
        self.assertEqual(len(self.storage.all(User)), 1)
        self.assertEqual(len(self.storage.all(Review)), 0)

    def test_new(self):
        """Test that new correctly adds an object"""
        self.storage.new(self.user)
        self.assertIn("User." + self.user.id, self.storage.all().keys())

    def test_save_to_file(self):
        """Test that save correctly saves objects to file storage"""
        self.storage.new(self.user)
        self.storage.save()
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        self.assertIn("User." + self.user.id, data.keys())

    def test_delete(self):
        """Test that delete correctly removes objects from storage"""
        self.storage.new(self.user)
        self.assertIn("User." + self.user.id, self.storage.all().keys())
        self.storage.delete(self.user)
        self.storage.save()
        self.assertNotIn("User." + self.user.id, self.storage.all().keys())

    def test_reload(self):
        """Test that reload correctly loads objects from storage"""
        self.storage.new(self.user)
        self.storage.save()
        self.storage.reload()
        objects = self.storage.all()
        self.assertIn("User." + self.user.id, objects.keys())

    def test_file_exists_after_save(self):
        """Ensure file exists after save"""
        self.storage.new(self.user)
        self.storage.save()
        self.assertTrue(os.path.isfile(self.file_path))

    def test_file_empty_on_initialization(self):
        """File should not exist on initialization if no save has been performed"""
        self.assertFalse(os.path.isfile(self.file_path))

    def test_storage_initialization(self):
        """Test that the file storage initializes correctly"""
        self.assertIsInstance(self.storage, type(storage))
