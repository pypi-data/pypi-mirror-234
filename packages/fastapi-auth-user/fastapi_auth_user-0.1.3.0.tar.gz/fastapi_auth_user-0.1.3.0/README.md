<p align="center">
 <img width="100px" src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI">
</p>
<p align="center">
    <em>Default auth service based on FastApi framework</em>
</p>

## Installation

<div class="termy">

```console
$ pip install fastapi-auth-user

or

for poetry:

$ poetry init
$ poetry add fastapi-auth-user
```
</div>

## Example

### Create it

* Create a file `main.py` with:

```Python
import uvicorn
from fastapi_auth_user import auth_app


if __name__ == "__main__":
    uvicorn.run(auth_app, host="localhost", port=3000)
```
### Run it

Run the server with:

<div class="termy">

```console
$ poetry run main.py or $ python3 main.py

INFO:  Started server process [12484]
INFO:  Waiting for application startup.
INFO:  Application startup complete.
INFO:  Uvicorn running on http://localhost:3000 (Press CTRL+C to quit)
```

</div>

### Check it

Open your browser at <a href="http://localhost:3000/docs" class="external-link" target="_blank">http://localhost:3000/docs.

You will see:
![img.png](images/img.png)

You already created an API that:

* All method __CRUD__ for __USER__ model`.
* All method __CRUD__ for __Role__ model`.
* Login user with oauth2
* Profile this user

## Env file
<div class="termy">

```console
DB_USER=<YOU USER NAME DB>                      #'postgres'
DB_PASSWORD=<YOU DATABASE PASSWORD>             #'root'
DB_HOST=<YOU DATABASE HOST>                     #'localhost'
DB_NAME=<YOU DATABASE NAME>                     #'auth_db'
DATABASE_URL=<YOU DATABASE URL>                 #'postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}'

ACCESS_TOKEN_EXPIRE_MINUTES=<TIME FOR TOKEN>    #30
SECRET_KEY=<SECRET KEY>                         #'secret_key'
ALGORITHM=<HASH ALGORITHM>                      #'HS256'
```

</div>