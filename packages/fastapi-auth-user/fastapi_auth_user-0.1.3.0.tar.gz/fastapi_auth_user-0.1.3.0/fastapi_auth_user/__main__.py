import argparse
from os import path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi_auth_user.auth import auth_router
from fastapi_auth_user.users import user_router

auth_app = FastAPI(title='AuthApi')

origins = [
	"http://localhost:3005",
	"https://localhost:3005",
	"http://localhost",
]

auth_app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--template", required=False, action=argparse.BooleanOptionalAction)
args = parser.parse_args()

if args.template:
	from fastapi_auth_user.page import page_router

	auth_app.mount("/static", StaticFiles(directory=path.dirname(path.realpath(__file__)) + r"/static"),
	               name="static")
	auth_app.include_router(page_router)

auth_app.include_router(user_router)
auth_app.include_router(auth_router)


def start():
	uvicorn.run('fastapi_auth_user.__main__:auth_app', host="localhost", port=3000, reload=True)
