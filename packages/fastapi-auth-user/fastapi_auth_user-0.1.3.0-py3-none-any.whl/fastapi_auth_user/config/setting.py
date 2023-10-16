import os

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings

load_dotenv(find_dotenv())


class Settings(BaseSettings):
	DB_USER: str | None = os.getenv("DB_USER")
	DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")
	DB_HOST: str | None = os.getenv("DB_HOST")
	DB_NAME: str | None = os.getenv("DB_NAME")
	DATABASE_URL: str = os.getenv("DATABASE_URL")

	SECRET_KEY: str = os.getenv("SECRET_KEY")
	ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
	ALGORITHM: str = os.getenv("ALGORITHM")

	def get_db_url(self) -> str:
		"""
		Return: url for connect database by .env variable
		"""
		return self.DATABASE_URL

	class Config:
		env_prefix: str = ""
		case_sensitive: bool = False
		env_file: str = ".env"
		env_file_encoding: str = "utf-8"


settings = Settings()
