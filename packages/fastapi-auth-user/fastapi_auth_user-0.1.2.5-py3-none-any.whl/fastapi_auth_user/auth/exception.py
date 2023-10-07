from fastapi_auth_user.models import RoleNameEnum


class PermissionException(Exception):
	def __init__(self, message: str, role: RoleNameEnum):
		self.message = message
		self.role = role
		super().__init__(self.message)
