"""DB module.
    Added add_user, find_user_by
    Echo: kept True
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password):
        """ Add a user to database. with email and password
        """
        self._session.add(User(email=email, hashed_password=hashed_password))
        self._session.commit()
        return self._session.query(User).filter(
                User.email == email and
                User.hashed_password == hashed_password).all()[0]

    def find_user_by(self, **args):
        for key in args:
            if not hasattr(User, key):
                raise InvalidRequestError
        a = self._session.query(User).filter_by(**args).all()
        if len(a) == 0:
            raise NoResultFound
        return a[0]
