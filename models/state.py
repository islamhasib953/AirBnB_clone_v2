#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models import storage_type


class State(BaseModel, Base):
    """State class"""

    __tablename__ = "states"
    if storage_type == "db":
        name = Column(String(128), nullable=False)
        cities = relationship(
            "City", back_populates="state", cascade="all, delete, delete-orphan"
        )

    else:
        name = ""

        @property
        def cities(self):
            data = []
            city_data = models.storage.all(cls=models.city)
            for key, value in city_data:
                if self.id == value.state_id:
                    data.append(value)
            return data
