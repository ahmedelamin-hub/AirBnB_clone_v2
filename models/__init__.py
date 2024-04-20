#!/usr/bin/python3
"""
Initialize the models package
"""
import os

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    from .engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from .engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
