from sqlalchemy.sql import func

from .base import engine, get_session
from .models import Category, Recipe, Type, User


def add_recipe(data):
    """Добавляет рецепты."""

    category, type_, title, text, author = (
        data["category"].strip(),
        data["type_"].strip(),
        data["title"].strip(),
        data["text"].strip(),
        data["author"],
    )

    current_session = get_session(engine)

    category = (
        current_session.query(Category)
        .filter(Category.title == category.capitalize())
        .first()
    )
    type_ = (
        current_session.query(Type)
        .filter(Type.title == type_.capitalize())
        .first()
    )
    author = (
        current_session.query(User)
        .filter(User.username == author["username"])
        .first()
    )
    new_recipe = Recipe(
        category_id=category.id,
        title=title,
        type_id=type_.id,
        text=text,
        author_id=author.id,
    )
    current_session.add(new_recipe)
    current_session.commit()


def get_recipes(data):
    """Получение нескольких элементов."""
    current_session = get_session(engine)

    category, type_ = data["category"].strip(), data["type_"].strip()

    category = (
        current_session.query(Category)
        .filter(Category.title == category.capitalize())
        .first()
    )
    type_ = (
        current_session.query(Type)
        .filter(Type.title == type_.capitalize())
        .first()
    )

    return (
        current_session.query(Recipe)
        .join(User)
        .join(Type)
        .join(Category)
        .filter(Recipe.category_id == category.id)
        .filter(Recipe.type_id == type_.id)
        .limit(data["amount"])
    )


def get_random_recipe():
    """Вывод рандомного элемента"""
    current_session = get_session(engine)
    return current_session.query(Recipe).order_by(func.random()).first()


def get_my_recipes(author):
    current_session = get_session(engine)
    user = current_session.query(User).filter(User.username == author).first()
    if user:
        return (
            current_session.query(Recipe)
            .filter(Recipe.author_id == user.id)
            .all()
        )
    return None


def get_categories():
    current_session = get_session(engine)
    return current_session.query(Category).all()


def get_types():
    current_session = get_session(engine)
    return current_session.query(Type).all()
