from typing import List, Optional

from fastapi import status

from .schema import LiteUser, UserCreate, UserUpdate
from ..database import BaseRepository, Database, RepositoryException
from ..models import User, RoleNameEnum, Role


class UserRepository(BaseRepository):
	def __init__(self, db: Database):
		super().__init__(db, User)

	def get_all(self, skip: int = 0, limit: int = 100) -> List[LiteUser]:
		return super().get_all(skip, limit)

	def create(self, obj_in: UserCreate) -> User:
		db_obj: User = User(**dict(obj_in))
		role_obj = self.get_role(RoleNameEnum.USER)

		db_obj.roles.append(role_obj)
		self.db.add(db_obj)
		self.db.commit()
		self.db.refresh(db_obj)
		return db_obj

	def get_by_id(self, user_id: int) -> User:
		return super().get_by_id(user_id)

	def update(self, obj_id: int, obj_in: UserUpdate) -> User:
		return super().update(obj_id, obj_in)

	def delete(self, user_id: int) -> User:
		return super().delete(user_id)

	def add_role(self, user_id: int, role: RoleNameEnum) -> User:
		role_obj = self.get_role(role)
		user: User = self.get_by_id(user_id)

		if not user:
			raise RepositoryException(status_code=status.HTTP_404_NOT_FOUND,
			                          message='Not found user with this id')

		if role_obj in user.roles:
			raise RepositoryException(status_code=status.HTTP_409_CONFLICT,
			                          message='User has this role')

		user.roles.append(role_obj)
		self.db.add(user)
		self.db.commit()
		self.db.refresh(user)
		return user

	def delete_role(self, user_id: int, role: RoleNameEnum) -> User:
		role_obj = self.get_role(role)
		user: User = self.get_by_id(user_id)
		if not user:
			raise RepositoryException(status_code=status.HTTP_409_CONFLICT,
			                          message='Not found user with this id')

		if len(user.roles) == 1:
			raise RepositoryException(status_code=status.HTTP_404_NOT_FOUND,
			                          message='User need have one role')

		if role_obj not in user.roles:
			raise RepositoryException(status_code=status.HTTP_404_NOT_FOUND,
			                          message='User hasnt this role')

		user.roles.remove(role_obj)
		self.db.add(user)
		self.db.commit()
		self.db.refresh(user)
		return user

	def get_role(self, role):
		role_obj = self.db.query(Role).filter(Role.name == role.value).first()
		if not role_obj:
			raise RepositoryException(status_code=status.HTTP_404_NOT_FOUND,
			                          message=f'Role [{role.value}] not created')

		return role_obj

	def get_user_by_email(self, email: Optional[str] = None) -> User:

		if email is None:
			raise RepositoryException(
				status_code=status.HTTP_404_NOT_FOUND,
				message=f'Wrong email!'
			)

		user: User = self.db.query(User).filter(User.email == email).first()

		return user

	def create_user_with_role(self, user: User, role: RoleNameEnum) -> User:
		role_obj = self.get_role(role)
		user.roles.append(role_obj)
		self.db.add(user)
		self.db.commit()
		self.db.refresh(user)
		return user

	def set_password(self, user_id: int, new_password: str) -> User:
		user = self.get_by_id(user_id)
		user.password = new_password
		self.db.commit()
		self.db.refresh(user)
		return user
