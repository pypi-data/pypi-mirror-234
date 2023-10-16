from os import path
from typing import Optional

from fastapi import HTTPException
from starlette.templating import Jinja2Templates, _TemplateResponse

from .context import RequestContext, ErrorContext, DataContext
from ..auth.permissions import auth_service
from ..database import Database, db_helper
from ..models import User, RoleNameEnum
from ..users import user_service
from ..users.schema import Token

templates_name = {
	'auth_panel': 'auth_panel.html',
	'user_panel': 'user_panel.html',
	'error_panel': 'error_panel.html',
}


class TemplateService:

	def __init__(
			self, db: Database
	):
		self.db = db
		self.templates = Jinja2Templates(
			directory="\\".join(path.dirname(path.realpath(__file__)).split("\\")[:-1]) + "\\templates")

	def generate_template(
			self, file_name: Optional[str], context: RequestContext
	) -> _TemplateResponse:
		try:
			if file_name is None:
				return self.generate_template_error(
					dict(request=context.get('request'), error=ValueError('Template is None'))
				)
			return self.templates.TemplateResponse(file_name, context=context)
		except Exception as err:
			errors = ". ".join(error[0].upper() + error[1:] for error in err.args)
			return self.generate_template_error(
				dict(request=context.get('request'), error=ValueError(f'"{errors}"'))
			)

	def generate_user_page_template(
			self, file_name: Optional[str], context: DataContext
	) -> _TemplateResponse:
		try:
			if file_name is None:
				return self.generate_template_error(
					dict(request=context.get('request'), error=ValueError('Template is None'))
				)

			token: Token = auth_service.get_access_token(self.db, context.get('data'))
			user: User = auth_service.get_user_by_token(self.db, token.access_token)

			users = user_service.get_all_users() if user_service.has_role(user, RoleNameEnum.ADMIN) else []

			return self.generate_template(file_name, context=dict(
				request=context.get('request'),
				token=token,
				user=user,
				users=users
			))

		except HTTPException as err:
			return self.generate_template_error(
				dict(request=context.get('request'), error=err)
			)

		except Exception as err:
			errors = ". ".join(error[0].upper() + error[1:] for error in err.args)
			return self.generate_template_error(
				dict(request=context.get('request'), error=ValueError(f'"{errors}"'))
			)

	def generate_template_error(
			self, context: ErrorContext
	) -> _TemplateResponse:
		return self.templates.TemplateResponse(templates_name.get('error_panel'), context=context)


template_service = TemplateService(next(db_helper.session_dependency()))
