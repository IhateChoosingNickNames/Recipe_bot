from sqlalchemy import create_engine
from .models import Base, Recipe, User, Category, Type
from sqlalchemy.orm import sessionmaker


def create_db():
    engine = create_engine("sqlite:///test_db.sqlite3")
    Base.metadata.create_all(bind=engine)


def populate_db():
    import json
    import datetime
    engine = create_engine("sqlite:///test_db.sqlite3")

    with open("static/data/test_data.json", encoding="UTF-8") as file:
        test_data = json.load(file)

    session = sessionmaker(bind=engine)
    current_session = session()

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
                elem["pub_date"] = datetime.datetime.fromisoformat(elem["pub_date"])
                print(elem["pub_date"])
            to_commit = curr_model(**elem)
            current_session.add(to_commit)
    current_session.commit()
