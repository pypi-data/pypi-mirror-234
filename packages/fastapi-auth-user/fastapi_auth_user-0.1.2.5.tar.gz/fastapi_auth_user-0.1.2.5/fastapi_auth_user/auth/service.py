from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from .user_forms import AuthUserDataForm
from ..config import settings
from ..database import Database, RepositoryException
from ..models import User
from ..users.repository import UserRepository
from ..users.schema import Token, UserAuth


class AuthenticationService:

	def __init__(self):
		self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
		self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login", scheme_name='scheme_name')

	def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> Token:
		to_encode = data.copy()
		if expires_delta:
			expire = datetime.utcnow() + expires_delta
		else:
			expire = datetime.utcnow() + timedelta(minutes=60)
		to_encode.update({"exp": expire})

		encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
		token: Token = Token(access_token=encoded_jwt)

		return token

	def password_hash(self, password: str) -> str:
		return self.pwd_context.hash(password)

	def verify_password(self, plain_password: str, hashed_password: str) -> bool:
		return self.pwd_context.verify(plain_password, hashed_password)

	def get_access_token(self, db: Database, user_data: AuthUserDataForm) -> Token:
		try:
			user = UserRepository(db).get_user_by_email(user_data.email)

			if user is None:
				raise RepositoryException(
					status_code=status.HTTP_404_NOT_FOUND,
					message=f'There is no user with that e-mail address.'
				)

			if not self.verify_password(user_data.password, user.password):
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
				                    detail="Wrong password")

			user_dict = UserAuth.from_orm(user).dict()
			token: Token = self.create_access_token(data=user_dict)
			return token

		except RepositoryException as err:
			raise err

		except HTTPException as http_err:
			raise http_err

		except Exception as err:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			                    detail="Internal server error")

	def get_user_by_token(self, db: Database, token: str) -> User:
		try:
			payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

			if payload is None:
				raise HTTPException(
					status_code=status.HTTP_401_UNAUTHORIZED,
					detail="Invalid authentication credentials",
					headers={"WWW-Authenticate": "Bearer"},
				)

			user = UserRepository(db).get_user_by_email(payload.get('email'))
			if user is None:
				raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
				                    detail="User not found")
			return user

		except JWTError:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Invalid authentication credentials",
				headers={"WWW-Authenticate": "Bearer"},
			)
