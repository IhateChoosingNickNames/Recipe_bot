from recipes.base import engine, get_session
from recipes.models import Base, Category, Recipe, Type, User
from settings import DATA_FILE


def create_db():
    """Создание необходимых таблиц в БД."""
    Base.metadata.create_all(bind=engine)


def populate_db():
    """Наполнение БД тестовыми данными."""
    import datetime
    import json

    with open(DATA_FILE, encoding="UTF-8") as file:
        test_data = json.load(file)

    schema = {
        "Users": User,
        "Categories": Category,
        "Types": Type,
        "Recipes": Recipe,
    }

    mapper = ["Types", "Categories", "Users", "Recipes"]
    for modelname, objects in sorted(
            test_data.items(), key=lambda x: mapper.index(x[0])
    ):
        current_session = get_session(engine)
        curr_model = schema[modelname]
        for elem in objects:

            # Если вручную задавать id, то не отработает автоинкремент.
            if "id" in elem:
                del elem["id"]

            if modelname == "Recipes":
                elem["pub_date"] = datetime.datetime.fromisoformat(
                    elem["pub_date"]
                )
            to_commit = curr_model(**elem)
            current_session.add(to_commit)

        current_session.commit()
