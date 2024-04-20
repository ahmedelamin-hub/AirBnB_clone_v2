#!/usr/bin/python3
"""
Unit test for the DBStorage class
"""

import unittest
from unittest.mock import patch
from models.engine.db_storage import DBStorage
from models.base_model import Base
from models.state import State
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class TestDBStorage(unittest.TestCase):
    """Test suite for DBStorage class."""

    @classmethod
    def setUpClass(cls):
        """Set up for the DB storage tests."""
        cls.user = 'hbnb_test'
        cls.password = 'hbnb_test_pwd'
        cls.host = 'localhost'
        cls.database = 'hbnb_test_db'
        cls.storage = DBStorage()
        cls.engine = create_engine(f'mysql+mysqldb://{cls.user}:{cls.password}@{cls.host}/{cls.database}')
        Base.metadata.create_all(cls.engine)

        # Ensure each test starts with a blank database
        Base.metadata.drop_all(cls.engine)
        Base.metadata.create_all(cls.engine)
        cls.session = scoped_session(sessionmaker(bind=cls.engine))

    @classmethod
    def tearDownClass(cls):
        """Finish with the DB storage tests."""
        cls.session.close()
        Base.metadata.drop_all(cls.engine)
        del cls.storage

    def test_new(self):
        """Test the 'new' method of DBStorage."""
        new_state = State(name="California")
        self.session.add(new_state)
        self.session.commit()
        self.assertIn(new_state, self.session)

    def test_all(self):
        """Test the 'all' method returns all objects when no class is passed."""
        new_state = State(name="California")
        self.session.add(new_state)
        self.session.commit()
        storage_dict = self.storage.all()
        self.assertIsInstance(storage_dict, dict)
        self.assertIn('State.{}'.format(new_state.id), storage_dict.keys())

    def test_delete(self):
        """Test the 'delete' method of DBStorage."""
        new_state = State(name="California")
        self.session.add(new_state)
        self.session.commit()
        self.assertIn(new_state, self.session)
        self.session.delete(new_state)
        self.session.commit()
        self.assertNotIn(new_state, self.session)

    def test_reload(self):
        """Test the 'reload' method restores all tables."""
        self.storage.reload()
        new_state = State(name="New York")
        self.session.add(new_state)
        self.session.commit()
        self.assertIn(new_state, self.session)

    def test_environment_test_drops_tables(self):
        """Test that tables are dropped if the environment is 'test'."""
        with patch.dict(os.environ, {'HBNB_ENV': 'test'}):
            self.storage.__init__()  # Reinitialize to simulate environment change
            self.assertIsNone(self.session.get(State, new_state.id))

if __name__ == "__main__":
    unittest.main()
