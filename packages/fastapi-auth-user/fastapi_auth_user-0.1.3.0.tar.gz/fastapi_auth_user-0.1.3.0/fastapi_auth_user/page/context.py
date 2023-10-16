from typing import TypedDict, Optional, Sequence

from fastapi import Request

from fastapi_auth_user.auth.user_forms import AuthUserDataForm
from fastapi_auth_user.models import User
from fastapi_auth_user.users.schema import Token


class RequestContext(TypedDict):
	request: Request


class ErrorContext(TypedDict):
	request: Request
	error: Exception


class DataContext(TypedDict):
	request: Request
	data: Optional[AuthUserDataForm]


class TokenUserContext(TypedDict):
	request: Request
	token: Token
	user: User
	users: Sequence[User]