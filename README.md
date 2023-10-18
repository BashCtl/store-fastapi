# Backend of pet store by using FastAPI
#### API has 3 routes
## 1) Users route
#### This route about CRUD users operations
## 2) Pets route
#### This route about add and manage pets in store
## 3) Store route
#### This route about place order for pets

## How to run locally
First clone this repo:
````
git clone git@github.com:bohdan-sk7/store-fastapi.git
````
Navigate to project dir:
````
cd store-fastapi
````
Install dependencies:
````
 pip install -r requirements.txt 
````
In the root of the project create .env file and specify following variables:
````
PROJECT_NAME=Store API
DB_URI=localhost
DB_NAME= name of databese
DB_PORT=5432
DB_USER= database user name
DB_PASS= database user password
SECRET_KEY=  secret string can be hash value
JWT_REFRESH_SECRET=secret string can be hash value
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_MINUTES=60*24*7
API_VERSION=v1
BACKEND_CORS_ORIGINS='["*"]'
ALLOW_METHODS='["*"]'
ALLOW_HEADERS='["*"]'
````
Download and install PostgreSQL database, [PostgreSQL](https://www.postgresql.org/download/)
Then create database specified in .env file DB_NAME

To start application run following command
````
uvicorn main:app --reload
````

You can use following link to view API documentation:
````
http://127.0.0.1:8000/docs 
````