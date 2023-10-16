from typing import List

from fastapi import status
from sqlalchemy.exc import IntegrityError

from .database import Database, ModelType
from .exception import RepositoryException
from ..models import User


class BaseRepository:

	def __init__(self, db: Database, model: ModelType):
		self.db = db
		self.model: ModelType = model

	def get_by_id(
			self,
			obj_id: int
	) -> ModelType:
		try:
			obj = self.db.query(self.model).filter(self.model.id == obj_id).first()
			if obj is None:
				raise RepositoryException(status_code=status.HTTP_404_NOT_FOUND,
				                          message=f"Record by this id({obj_id}) not found")
			else:
				return obj

		except RepositoryException as re:
			self.db.rollback()
			raise re
		except IntegrityError as _:
			self.db.rollback()
			raise RepositoryException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			                          message=f"Operation failed | ORM")
		except Exception as err:
			self.db.rollback()
			raise RepositoryException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			                          message=f"Detail: '{err.args[0]}'")

	def get_all(
			self,
			skip: int = 0,
			limit: int = 100
	) -> List[ModelType]:
		try:

			if skip < 0 or limit < 0:
				raise RepositoryException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
				                          message=f"Incorrect skip({skip}) or limit({limit})")

			objs = self.db.query(self.model).offset(skip).limit(limit).all()
			if objs is None or not len(objs):
				raise RepositoryException(status_code=status.HTTP_400_BAD_REQUEST, message=f"No records")
			else:
				return objs
		except RepositoryException as re:
			self.db.rollback()
			raise re
		except IntegrityError as _:
			self.db.rollback()
			raise RepositoryException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			                          message=f"Operation failed | ORM")
		except Exception as err:
			raise RepositoryException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			                          message=f"Detail: '{err.args[0]}'")

	def create(
			self,
			obj_in: ModelType
	) -> ModelType:
		try:
			db_obj: User = self.model(**dict(obj_in))

			if not db_obj:
				raise RepositoryException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				                          message='Create object error')

			self.db.add(db_obj)
			self.db.commit()
			self.db.refresh(db_obj)

			return db_obj
		except RepositoryException as re:
			self.db.rollback()
			raise re
		except IntegrityError as _:
			self.db.rollback()
			raise RepositoryException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			                          message="Operation failed | ORM")
		except Exception as err:
			self.db.rollback()
			raise RepositoryException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			                          message=f"Detail: '{err.args[0]}'")

	def update(
			self,
			obj_id: int,
			obj_in: ModelType
	) -> ModelType:
		try:
			db_user: ModelType = self.get_by_id(obj_id)
			if not db_user:
				raise RepositoryException(status_code=status.HTTP_404_NOT_FOUND,
				                          message=f"Update failed, record with id({obj_id}) not found")

			for field_name, field_value in obj_in.dict(exclude_unset=True).items():
				setattr(db_user, field_name, field_value)

			self.db.commit()
			self.db.refresh(db_user)
			return db_user
		except IntegrityError as _:
			self.db.rollback()
			raise RepositoryException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			                          message="Update failed due to integrity constraint violation.")
		except Exception as err:
			self.db.rollback()
			raise RepositoryException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			                          message=f"Update failed. {err.args[0]}")

	def delete(
			self,
			obj_id: int
	) -> ModelType:
		try:
			row_to_delete = self.get_by_id(obj_id)

			if not row_to_delete:
				raise RepositoryException(status_code=status.HTTP_404_NOT_FOUND,
				                          message="Delete failed, record with id({obj_id}) not found")

			self.db.delete(row_to_delete)
			self.db.commit()
			return row_to_delete
		except RepositoryException as re:
			self.db.rollback()
			raise re
		except IntegrityError as _:
			self.db.rollback()
			raise RepositoryException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			                          message="Delete failed due to integrity constraint violation.")
		except Exception as err:
			self.db.rollback()
			raise RepositoryException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			                          message=f"Delete failed due to an unknown error. {err.args[0]}")
