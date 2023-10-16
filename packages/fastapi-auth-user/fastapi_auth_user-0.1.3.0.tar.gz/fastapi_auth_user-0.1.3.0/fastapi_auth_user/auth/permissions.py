from typing import Union, List

from fastapi import Depends, HTTPException, status

from .exception import PermissionException
from .service import AuthenticationService
from ..database import db_helper
from ..models import RoleNameEnum, User

auth_service = AuthenticationService(next(db_helper.session_dependency()))


class RolePermissions:
	def __init__(self, roles: List[RoleNameEnum]):
		self.roles = roles

	def get_permissions(
			self,
			token: str = Depends(auth_service.oauth2_scheme)
	) -> Union[bool, PermissionException]:
		try:
			current_user: User = auth_service.get_user_by_token(token)
			for role in self.roles:
				for user_role in current_user.roles:
					if role.value == user_role.name:
						return True
			else:
				raise PermissionException(message=f'Permission denied', role=str(self))
		except PermissionException as err:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

		except Exception:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission denied")

	def __repr__(self) -> str:
		return f"RolePermissions([{','.join(role.value for role in self.roles)}])"
