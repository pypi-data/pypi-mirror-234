from sqlalchemy import (
	Column,
	Integer,
	String,
	ForeignKey,
	Table,
	DefaultClause
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Define a many-to-many association table between users and roles
user_role_association = Table(
	"user_role_association",
	Base.metadata,
	Column("user_id", Integer, ForeignKey("users.id")),
	Column("role_id", Integer, ForeignKey("roles.id"), server_default=DefaultClause('2')),
)


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, index=True)
	email = Column(String, unique=True, index=True)
	password = Column(String)

	# Define a many-to-many relationship between users and roles
	roles = relationship("Role", secondary=user_role_association, back_populates="users")


class Role(Base):
	__tablename__ = "roles"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, unique=True, index=True)

	# Define a back-reference to access users associated with this role
	users = relationship("User", secondary=user_role_association, back_populates="roles")
