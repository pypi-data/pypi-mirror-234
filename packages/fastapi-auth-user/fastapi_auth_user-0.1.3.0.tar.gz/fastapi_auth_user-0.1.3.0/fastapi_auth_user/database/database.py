from ..config import settings
from .exception import DataException
from sqlalchemy import create_engine
from sqlalchemy.orm import (
	sessionmaker,
	Session
)
from ..models import Base
from typing import TypeAlias

Database: TypeAlias = Session
ModelType: TypeAlias = Base


class DatabaseHelper:
	def __init__(self, url: str):
		self.__engine = create_engine(url)
		self.__session_factory = sessionmaker(
			bind=self.__engine,
			autoflush=False,
			autocommit=False,
			expire_on_commit=False,
		)

	def session_dependency(self) -> Database:
		with self.__session_factory() as session:
			yield session

	def create_all_tables(self):
		Base.metadata.create_all(bind=self.__engine)

	def create_role_initial(self):
		from .db_utils import create_role_initial
		try:
			create_role_initial(self.__session_factory())
		except DataException as err:
			raise err


db_helper = DatabaseHelper(
	settings.get_db_url()
)
