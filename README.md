# Performers and Songs

This is a RESTFUL API for cooperation with a database of performers, albums and songs.
Supports all CRUD operations with filtering, pagination and authentication.

## Features

- Full CRUD operations using HTTP-methods: GET, POST, PUT, PATCH and DELETE
- User authentication
- Filtering by some basic parameters
- Pagination support

## Tech Stack

- **Python 3.12** – Main programming language
- **FastAPI** – For building the web API
- **PostgreSQL** – For the database
- **SQLModel** – For ORM and schema definitions
- **Alembic** – For database migrations
- **Pydantic** – For validation and serialization
- **Uvicorn** – ASGI for running the app
- **FastAPI Users** – Library for authentication and user management

## Installation and running the project

**1. Clone the repository and navigate into the Project folder**

```
git clone https://github.com/rifemane5328/Performers-and-songs.git
cd Performers-and-songs
```

**2. Install dependencies**

```
pip install -r requirements.txt
```

**3. Create the database**  
To create and manage your PostgreSQL database, download [PgAdmin](https://www.pgadmin.org/download).
After installing, sing in and create a new database
You can name it anything you like, but make sure to use the same name in your `.env` file.

**4. Create and fill out the .env file**  
Create a `.env` file in the root of your project  
Use the following settings: 

```
BE_DEBUG=true
BE_DATABASE__HOST=localhost
BE_DATABASE__PORT=your_database_port
BE_DATABASE__DB=your_db_name
BE_DATABASE__USER=postgres
BE_DATABASE__PASSWORD=your_db_password
BE_DATABASE__ENGINE=postgresql+asyncpg
BE_DATABASE__DEBUG=true

BE_AUTH__RESET_PASSWORD_TOKEN_SECRET="your_reset_token"
BE_AUTH__VERIFICATION_TOKEN_SECRET="your_verification_token"
BE_AUTH__JWT_STRATEGY_TOKEN_SECRET="your_jwt_token"
```

**5. Run the migrations**  
Generate and apply the migrations with the following commands:
```
alembic revision --autogenerate -m 'initial'
alembic upgrade head
```

**6. Run the project**  
To run the project, use the following command:

```
uvicorn main:app --reload
```
If the default port isn't working, try to use a different one with the `--port` option.  
For example:  

```
uvicorn main:app --port 8001 --reload
```
