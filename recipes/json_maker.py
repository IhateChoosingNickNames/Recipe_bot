import sqlite3

con = sqlite3.connect("db.sqlite3")
curr = con.cursor()

lst = ["recipes_recipe", "recipes_type", "recipes_category"]
models = {"recipe": "Recipes", "type": "Types", "category": "Categories"}

mapper = {
    "Recipes": {
        "id": None,
        "title": None,
        "text": None,
        "pub_date": None,
        "category_id": None,
        "type_id": None,
        "user_id": None,
    },
    "Types": {
        "id": None,
        "title": None,
    },
    "Categories": {
        "id": None,
        "title": None,
    },
    "Users": {
        "id": 6,
        "username": "Test_user",
        "first_name": None,
        "last_name": None,
        "email": None,
    },
}

result = {
    "Recipes": [],
    "Types": [],
    "Categories": [],
    "Users": [
        {
            "id": 6,
            "username": "Test_user",
            "first_name": None,
            "last_name": None,
            "email": None,
        },
    ],
}

for table in lst:
    res = curr.execute(f"SELECT * FROM {table}")
    model = table.split("_")[1]
    curr_model = models[model]
    for row in res:
        tmp = dict(zip(mapper[curr_model].keys(), row))
        result[curr_model].append(tmp)

import json

print(result["Types"])

with open("SqlAlchemy/test_data.json", "w", encoding="UTF-8") as file:
    json.dump(result, file)
