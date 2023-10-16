# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_auth_user',
 'fastapi_auth_user.auth',
 'fastapi_auth_user.config',
 'fastapi_auth_user.database',
 'fastapi_auth_user.models',
 'fastapi_auth_user.page',
 'fastapi_auth_user.static',
 'fastapi_auth_user.templates',
 'fastapi_auth_user.users']

package_data = \
{'': ['*'], 'fastapi_auth_user.static': ['css/*']}

install_requires = \
['alembic>=1.12.0,<2.0.0',
 'bcrypt>=4.0.1,<5.0.0',
 'fastapi>=0.95.0,<0.96.0',
 'jinja2>=3.1.2,<4.0.0',
 'passlib>=1.7.4,<2.0.0',
 'psycopg2-binary>=2.9.7,<3.0.0',
 'psycopg2>=2.9.7,<3.0.0',
 'pyjwt>=2.6.0,<3.0.0',
 'python-decouple>=3.8,<4.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'python-jose>=3.3.0,<4.0.0',
 'python-multipart>=0.0.6,<0.0.7',
 'sqlalchemy>=2.0.8,<3.0.0',
 'uvicorn>=0.21.1,<0.22.0']

entry_points = \
{'console_scripts': ['start = fastapi_auth_user.__main__:start']}

setup_kwargs = {
    'name': 'fastapi-auth-user',
    'version': '0.1.3.0',
    'description': 'auth user',
    'long_description': '<p align="center">\n <img width="100px" src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI">\n</p>\n<p align="center">\n    <em>Default auth service based on FastApi framework</em>\n</p>\n\n## Installation\n\n<div class="termy">\n\n```console\n$ pip install fastapi-auth-user\n\nor\n\nfor poetry:\n\n$ poetry init\n$ poetry add fastapi-auth-user\n```\n</div>\n\n## Example\n\n### Create it\n\n* Create a file `main.py` with:\n\n```Python\nimport uvicorn\nfrom fastapi_auth_user import auth_app\n\n\nif __name__ == "__main__":\n    uvicorn.run(auth_app, host="localhost", port=3000)\n```\n### Run it\n\nRun the server with:\n\n<div class="termy">\n\n```console\n$ poetry run main.py or $ python3 main.py\n\nINFO:  Started server process [12484]\nINFO:  Waiting for application startup.\nINFO:  Application startup complete.\nINFO:  Uvicorn running on http://localhost:3000 (Press CTRL+C to quit)\n```\n\n</div>\n\n### Check it\n\nOpen your browser at <a href="http://localhost:3000/docs" class="external-link" target="_blank">http://localhost:3000/docs.\n\nYou will see:\n![img.png](images/img.png)\n\nYou already created an API that:\n\n* All method __CRUD__ for __USER__ model`.\n* All method __CRUD__ for __Role__ model`.\n* Login user with oauth2\n* Profile this user\n\n## Env file\n<div class="termy">\n\n```console\nDB_USER=<YOU USER NAME DB>                      #\'postgres\'\nDB_PASSWORD=<YOU DATABASE PASSWORD>             #\'root\'\nDB_HOST=<YOU DATABASE HOST>                     #\'localhost\'\nDB_NAME=<YOU DATABASE NAME>                     #\'auth_db\'\nDATABASE_URL=<YOU DATABASE URL>                 #\'postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}\'\n\nACCESS_TOKEN_EXPIRE_MINUTES=<TIME FOR TOKEN>    #30\nSECRET_KEY=<SECRET KEY>                         #\'secret_key\'\nALGORITHM=<HASH ALGORITHM>                      #\'HS256\'\n```\n\n</div>',
    'author': 'Vittalius',
    'author_email': 'Vittalius@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
