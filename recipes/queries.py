from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from .models import Recipe, Category, Type, User


def set_connection():
    engine = create_engine("sqlite:///test_db.sqlite3")
    session = sessionmaker(bind=engine)
    return session()


def add_recipe(data):
    '''Добавляет рецепты.'''
    print(data)
    category, type_, title, text, author = data["category"].strip(), data["type_"].strip(), data["title"].strip(), data["text"].strip(), data["author"]

    current_session = set_connection()

    category = current_session.query(Category).filter(Category.title == category.capitalize()).first()
    type_ = current_session.query(Type).filter(Type.title == type_.capitalize()).first()
    author = current_session.query(User).filter(User.username==author["username"]).first()

    new_recipe = Recipe(category_id=category.id, title=title, type_id=type_.id, text=text, author_id=author.id)
    current_session.add(new_recipe)
    current_session.commit()


def get_recipe(amount):
    """Получение нескольких элементов."""
    current_session = set_connection()
    return current_session.query(Recipe).join(User).join(Type).join(Category).limit(amount)


def get_random_recipe():
    """Вывод рандомного элемента"""
    current_session = set_connection()
    return current_session.query(Recipe).order_by(func.random()).first()


def get_my_recipes(author):
    current_session = set_connection()
    user = current_session.query(User).filter(User.username==author).first()
    if user:
        return current_session.query(Recipe).filter(Recipe.author_id==user.id).all()


def get_categories():
    current_session = set_connection()
    return current_session.query(Category).all()


def get_types():
    current_session = set_connection()
    return current_session.query(Type).all()
