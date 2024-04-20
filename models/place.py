#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    user = relationship("User", back_populates="places")
    city = relationship("City", back_populates="places")
    reviews = relationship("Review", back_populates="place", cascade="all, delete")

    if 'HBNB_TYPE_STORAGE' not in globals() or HBNB_TYPE_STORAGE != 'db':
        @property
        def reviews(self):
            """Returns the list of Review instances with place_id equals to the current Place.id"""
            from models import storage
            all_reviews = storage.all(Review)
            place_reviews = [review for review in all_reviews.values() if review.place_id == self.id]
            return place_reviews
