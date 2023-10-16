from typing import TypedDict, Optional

from fastapi import Request

from fastapi_auth_user.auth.user_forms import AuthUserDataForm


class RequestContext(TypedDict):
	request: Request


class ErrorContext(TypedDict):
	request: Request
	error: Exception


class DataContext(TypedDict):
	request: Request
	data: Optional[AuthUserDataForm]