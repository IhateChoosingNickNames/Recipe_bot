from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class Recipe(Base):
    __tablename__ = "Recipes"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    text = Column(String)
    pub_date = Column(DateTime(timezone=True), server_default=func.now())
    category_id = Column(Integer, ForeignKey("Categories.id"))
    Category = relationship("Category", foreign_keys="Recipe.category_id")
    type_id = Column(Integer, ForeignKey("Types.id"))
    Type = relationship("Type", foreign_keys="Recipe.type_id")
    author_id = Column(Integer, ForeignKey("Users.id"))
    author = relationship("User", foreign_keys="Recipe.author_id")

    def __repr__(self):
        return (f"id={self.id!r}, title={self.title[:15]!r}, "
                f"author={self.author.username!r}")


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    recipe = relationship("Recipe", back_populates="author")

    def __repr__(self):
        return f"id={self.id!r}, username={self.username[:15]!r}"


class Category(Base):
    __tablename__ = "Categories"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    recipe = relationship("Recipe", back_populates="Category")

    def __repr__(self):
        return f"id={self.id!r}, title={self.title[:15]!r}"


class Type(Base):
    __tablename__ = "Types"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    recipe = relationship("Recipe", back_populates="Type")

    def __repr__(self):
        return f"id={self.id!r}, title={self.title[:15]!r}"
