from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings

load_dotenv(find_dotenv())


class Settings(BaseSettings):
	DB_USER: str | None
	DB_PASSWORD: str | None
	DB_HOST: str | None
	DB_NAME: str | None
	DATABASE_URL: str

	SECRET_KEY: str
	ALGORITHM: str

	def get_db_url(self) -> str:
		"""
		Return: url for connect database by .env variable
		"""
		return self.DATABASE_URL


settings = Settings()
