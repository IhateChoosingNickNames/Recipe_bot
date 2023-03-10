# Recipe_bot

Description: Bot for getting/adding recipes.
Simple bot for learning SQLAlchemy, Docker, Postgres and Poetry


Used technologies:
-
    - python 3.10.4
    - SQLAlchemy 2.0.4
    - requests 2.26.0
    - pyTelegramBotAPI 4.10.0
    - dotenv 0.21.1
    - Docker 20.10.22
Features:
-
    - You can get recipe by category/type with required amount
    - You can add new recipe in existing category/type
    - You can view list of your
    - You can get random recipe
    - You can prepopulate DB with JSON-file
    - Add admins
    - Admins can now add new types and categories

Instructions:
-
## enviroment:
Create .env file in root/Recipe_bot directory and fill it with required keys:

### Bot token is requiered to launch:
- TG_BOT=...
### Postgres settings:
- DB_ENGINE=...
- DB_NAME=...
- POSTGRES_USER=...
- POSTGRES_PASSWORD=...
- DB_HOST=...(use <db> if you want to run this app via docker)
- DB_PORT=...
### Path to json-file for populating DB:
- DATA=...


## Local launch:

1. Install requirements:
    #### pip install -r requirements.txt
2. Go to manage.by directory and create db:
    #### python manage.py create_db
3. Fill the DB with prepared CSV-files:
    #### python manage.py populate_db
4. Start bot:
    #### python manage.py start_bot


## Docker:
1. Make docker-build:
    #### docker-compose up -d --build
2. Create required tables:
    #### docker-compose exec web python manage.py create_db
3. Prepopulate DB with prepared data:
    ####  docker-compose exec web python manage.py populate_db


For now app's ready to use.


Examples of comands:
-
  - /start
  - /menu
  - /get_random_recipe
  - /admin