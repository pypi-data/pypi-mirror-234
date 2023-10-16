
from .database import Database
from fastapi_auth_user.models import Role, RoleNameEnum


def create_role_initial(db: Database):
	for role_name in RoleNameEnum:
		is_role_exist = db.query(Role).filter_by(name=role_name.value).first() is not None
		if not is_role_exist:
			role = Role(name=role_name.value)
			db.add(role)
			db.commit()
