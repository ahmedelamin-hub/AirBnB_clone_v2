#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey, MetaData
from sqlalchemy.orm import relationship


# Define the metadata instance
metadata = Base.metadata

# Association Table for Many-to-Many relationship between Place and Amenity
place_amenity = Table('place_amenity', metadata,
                      Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
                      )


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
    amenities = relationship("Amenity", secondary=place_amenity, back_populates="place_amenities", viewonly=False)

    @property
    def amenities(self):
        """Get list of Amenity instances from amenity_ids."""
        return [amenity for amenity in self.amenity_ids]

    @amenities.setter
    def amenities(self, obj):
        """If obj is an Amenity, adds its ID to amenity_ids."""
        if isinstance(obj, Amenity):
            if obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
