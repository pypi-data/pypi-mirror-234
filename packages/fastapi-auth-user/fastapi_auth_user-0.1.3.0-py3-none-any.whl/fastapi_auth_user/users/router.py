from typing import List

from fastapi import APIRouter, Depends, status

from .schema import (
	UserCreate,
	UserTokenResponse,
	LiteUser,
	UserUpdate, UserRoles
)
from .service import UserService
from ..auth.permissions import RolePermissions
from ..database import db_helper
from ..models import RoleNameEnum

user_router = APIRouter(
	prefix='/api',
	tags=["Users"],
	dependencies=[],
	responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

permissions_admin_moderator = RolePermissions([RoleNameEnum.ADMIN, RoleNameEnum.Moderator])
permissions_user = RolePermissions([RoleNameEnum.USER])

user_service = UserService(next(db_helper.session_dependency()))


@user_router.get("/", response_model=List[LiteUser])
def get_users(
		skip: int = 0,
		limit: int = 10,
		access: bool = Depends(permissions_user.get_permissions)
):
	return user_service.get_all_users(skip, limit)


@user_router.get("/{user_id}", response_model=LiteUser)
def get_user(
		user_id: int = 1,
		access: bool = Depends(permissions_user.get_permissions)
):
	return user_service.get_by_id(user_id)


@user_router.post("/", response_model=UserTokenResponse, status_code=201)
def create_user(
		user: UserCreate,
		access: bool = Depends(permissions_admin_moderator.get_permissions)
):
	return user_service.create(user)


@user_router.patch("/{user_id}", response_model=UserTokenResponse)
def update_user(
		user_id: int,
		user: UserUpdate,
		access: bool = Depends(permissions_admin_moderator.get_permissions)
):
	return user_service.update(user_id, user)


@user_router.delete("/{user_id}", response_model=LiteUser)
def delete_user(
		user_id: int,
		access: bool = Depends(permissions_admin_moderator.get_permissions)
):
	return user_service.delete(user_id)


@user_router.get("/user/role/{user_id}", response_model=UserRoles)
def get_user_roles(
		user_id: int,
		access: bool = Depends(permissions_admin_moderator.get_permissions)
):
	return user_service.get_user_roles(user_id)


@user_router.post("/user/role/{user_id}", response_model=UserRoles)
def add_user_role(
		user_id: int,
		role: RoleNameEnum,
		access: bool = Depends(permissions_admin_moderator.get_permissions)
):
	return user_service.add_role_for_user(user_id, role)


@user_router.delete("/user/role/{user_id}", response_model=UserRoles)
def add_user_role(
		user_id: int,
		role: RoleNameEnum,
		access: bool = Depends(permissions_admin_moderator.get_permissions)
):
	return user_service.delete_user_role(user_id, role)
