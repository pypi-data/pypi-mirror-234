from fastapi import APIRouter, Depends, status
from starlette.templating import Jinja2Templates

from .service import AuthenticationService
from .user_forms import AuthUserDataForm
from ..database import db_helper, Database
from ..users.schema import Token, UserAuth

auth_router = APIRouter(
	prefix='/api',
	tags=["Authentication"],
	dependencies=[],
	responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

auth_service = AuthenticationService()


@auth_router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login_user(
		user_data: AuthUserDataForm = Depends(AuthUserDataForm.as_form),
		db: Database = Depends(db_helper.session_dependency)
):
	user_data.email = user_data.username if user_data.email is None else user_data.email
	return auth_service.get_access_token(db, user_data)


@auth_router.get("/profile/me", response_model=UserAuth, status_code=status.HTTP_201_CREATED)
def get_user_by_token(
		token: str = Depends(auth_service.oauth2_scheme),
		db: Database = Depends(db_helper.session_dependency)
):
	return auth_service.get_user_by_token(db, token)


templates = Jinja2Templates(directory="templates")
