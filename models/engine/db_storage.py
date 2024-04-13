from sqlalchemy import create_engine
import os
from models.base_model import Base, BaseModel
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    __engine = None
    __session = None
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

    def __init__(self):
        """Instatiate the engine and drop if test database"""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                os.environ["HBNB_MYSQL_USER"],
                os.environ["HBNB_MYSQL_PWD"],
                os.environ["HBNB_MYSQL_HOST"],
                os.environ["HBNB_MYSQL_DB"],
            ),
            pool_pre_ping=True,
        )
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        data_obj = {}
        if cls is None:
            obj = self.__session.query(Amenity, City, Place, Review, State, User).all()
        else:
            cls = self.classes[cls]
            if cls is None:
                return data_obj
            else:
                obj = self.__session.query(cls).all()

        for object in obj:
            key = object.__class__.__name__ + "." + object.id
            value = object
            data_obj[key] = value
        return data_obj

    def new(self, obj):
        self.__session.add(obj)
        self.__session.flush()

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)
            self.__session.commit()

    def reload(self):
        Base.metadata.create_all(self.__engine)
        some_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(some_factory)

        self.__session = Session()
