#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column("id", String(60), nullable=False, primary_key=True)
    # created_at = Column("created_at", default=datetime.utcnow(), nullable=False)
    # updated_at = Column("updated_at", default=datetime.utcnow(), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if kwargs and "id" not in self.__dict__:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
        elif kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split(".")[-1]).split("'")[0]
        return "[{}] ({}) {}".format(cls, self.id, self.__dict__)

    def __repr__(self):
        """return a string representaion"""
        return self.__str__()

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in my_dict.keys():
            del my_dict["_sa_instance_state"]
        return my_dict

    def delete(self):
        models.storage.delete(self)
