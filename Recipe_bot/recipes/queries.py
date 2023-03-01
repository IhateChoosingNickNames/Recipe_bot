from sqlalchemy.sql import func

from .base import engine, get_session
from .exceptions import NoRecipesFoundError
from .models import Category, Recipe, Type, User


def get_or_create(session, model, **kwargs):
    """Достать пользователя из БД или создать нового."""
    instance = session.query(model).filter(User.username == kwargs["username"]).first()

    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()

    return instance


def add_recipe(data):
    """Добавление рецептов."""

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
    author = get_or_create(current_session, User, username=author["username"])

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
        .order_by(Recipe.title)
        .limit(data["amount"])
    )


def get_random_recipe():
    """Получение рандомного рецепта."""
    current_session = get_session(engine)
    return current_session.query(Recipe).order_by(func.random()).first()


def get_my_recipes(author):
    """Получение рецептов текущего пользователя."""
    current_session = get_session(engine)
    user = current_session.query(User).filter(User.username == author).first()

    if not user:
        raise NoRecipesFoundError

    return (
        current_session.query(Recipe)
        .filter(Recipe.author_id == user.id)
    )


def get_categories():
    """Получение всех категорий."""
    current_session = get_session(engine)
    return current_session.query(Category).order_by(Category.title).all()


def get_types():
    """Получение всех типов."""
    current_session = get_session(engine)
    return current_session.query(Type).order_by(Type.title).all()


def get_user(data):
    """Получение пользователя."""
    current_session = get_session(engine)
    user = get_or_create(current_session, User, **data)
    return user


def create_type_or_category(data):
    """Создание категории или типа."""

    current_session = get_session(engine)

    if data["is_type"]:
        tmp = Type(title=data["title"])
    else:
        tmp = Category(title=data["title"])

    current_session.add(tmp)
    current_session.commit()
