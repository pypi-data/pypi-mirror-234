import re
from datetime import datetime
from typing import List

from pydantic import (
	BaseModel,
	Field,
	validator
)


class UserBase(BaseModel):
	username: str = Field(..., min_length=5)
	email: str = Field(..., min_length=5)

	@validator("email")
	def validate_email(cls, value):
		email_regex = r'^[\w\.-]+@[\w\.-]+$'
		if not re.match(email_regex, value):
			raise ValueError("Invalid email address format")
		return value

	class Config:
		orm_mode = True


class UserCreate(UserBase):
	password: str = Field(..., min_length=5)

	@validator("password")
	def validate_email(cls, value):
		password_regex = r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{5,25})'
		if not re.match(password_regex, value):
			raise ValueError("Invalid password address format")
		return value

	class Config:
		orm_mode = True


UserAuth = UserCreate


class LiteUser(UserBase):
	id: int

	class Config:
		orm_mode = True


class Token(BaseModel):
	token_time: datetime
	token: str


class RefreshToken(BaseModel):
	refresh_token: str = Field(default='Refresh token', title="Refresh token", min_length=5)


class Tokens(BaseModel):
	access_token: Token
	refresh_token: Token


class TokenData(BaseModel):
	access_token_time: datetime
	access_token: str
	refresh_token: str
	refresh_token_time: datetime


class UserToken(LiteUser):
	token: Token


class UserRole(BaseModel):
	id: int = None
	name: str

	class Config:
		orm_mode = True


class UserRoles(BaseModel):
	id: int
	roles: List[UserRole]

	class Config:
		orm_mode = True


class UserTokenResponse(UserToken, LiteUser):
	class Config:
		orm_mode = True


class UserUpdate(BaseModel):
	id: int = None
	username: str = None
	email: str = None
	password: str = None

	class Config:
		orm_mode = True
