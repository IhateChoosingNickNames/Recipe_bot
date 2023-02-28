from Recipe_bot.recipes.base import engine, get_session
from Recipe_bot.recipes.models import Base, Category, Recipe, Type, User
from Recipe_bot.settings import DATA_FILE


def create_db():
    Base.metadata.create_all(bind=engine)


def populate_db():
    import datetime
    import json

    with open(DATA_FILE, encoding="UTF-8") as file:
        test_data = json.load(file)

    current_session = get_session(engine)

    schema = {
        "Users": User,
        "Categories": Category,
        "Types": Type,
        "Recipes": Recipe,
    }

    for modelname, objects in test_data.items():
        curr_model = schema[modelname]
        for elem in objects:
            if modelname == "Recipes":
                elem["pub_date"] = datetime.datetime.fromisoformat(
                    elem["pub_date"]
                )
            to_commit = curr_model(**elem)
            current_session.add(to_commit)

    current_session.commit()
