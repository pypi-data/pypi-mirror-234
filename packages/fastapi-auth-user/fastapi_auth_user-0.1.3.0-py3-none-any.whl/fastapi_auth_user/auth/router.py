from fastapi import APIRouter, Depends, status

from .user_forms import AuthUserDataForm, ResetUserPasswordDataForm
from ..database import db_helper
from ..users.schema import Tokens, Token, UserAuth, LiteUser, RefreshToken, TokenData
from .service import AuthenticationService

auth_router = APIRouter(
	prefix='/api',
	tags=["Authentication"],
	dependencies=[],
	responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

auth_service = AuthenticationService(next(db_helper.session_dependency()))


@auth_router.post("/login", response_model=TokenData, status_code=status.HTTP_200_OK)
def login_user(
		user_data: AuthUserDataForm = Depends(AuthUserDataForm.as_form),
):
	user_data.email = user_data.username if user_data.email is None else user_data.email
	tokens: Tokens = auth_service.get_tokens(user_data)
	return TokenData(
		access_token_time=tokens.access_token.token_time,
		access_token=tokens.access_token.token,
		refresh_token_time=tokens.refresh_token.token_time,
		refresh_token=tokens.refresh_token.token,
	)


@auth_router.get("/profile/me", response_model=UserAuth, status_code=status.HTTP_201_CREATED)
def get_user_by_token(
		token: str = Depends(auth_service.oauth2_scheme),
):
	return auth_service.get_user_by_token(token)


@auth_router.post("/reset-password", response_model=LiteUser, status_code=status.HTTP_201_CREATED)
def reset_password(
		token: str = Depends(auth_service.oauth2_scheme),
		user_data: ResetUserPasswordDataForm = Depends(ResetUserPasswordDataForm.as_form),
):
	return auth_service.reset_password(token, user_data.new_password)


@auth_router.post("/refresh-token", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh_token(
		token: RefreshToken
):
	return auth_service.refresh_access_token(token)
