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
    'version': '0.1.2.3',
    'description': 'auth user',
    'long_description': '<p align="center">\n <img width="100px" src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI">\n</p>\n<p align="center">\n    <em>Default auth service based on FastApi framework</em>\n</p>',
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
