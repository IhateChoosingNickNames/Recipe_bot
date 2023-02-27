import datetime
import json

import requests
import telebot
from telebot import types

from recipes.queries import get_recipe, add_recipe, get_random_recipe, get_types, get_categories, get_my_recipes
from dotenv import load_dotenv
import os

from recipes.exceptions import WrongInputError
from .help_stuff import show_result, parse_input, \
    show_available_cats_and_types, validate_author_fields

load_dotenv()
SECRET_KEY = os.getenv("TG_BOT")
bot = telebot.TeleBot(SECRET_KEY)


commands = ["/get_recipe", "/add_recipe", "/menu", "/start", "/get_random_recipe", "/my_recipes"]
recipe = {"params": None}


def start_bot():
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.infinity_polling()


@bot.message_handler(commands=['my_recipes'])
def bot_my_recipes(request):
    """Фунция приветствия."""
    bot.delete_message(request.chat.id, request.message_id)
    result = get_my_recipes(request.from_user.username)
    bot.send_message(request.chat.id, f'Вывожу посты пользователя {request.from_user.first_name}!', parse_mode='HTML')
    show_result(bot, result, request)


@bot.message_handler(commands=['start'])
def bot_start(request):
    """Фунция приветствия."""

    bot.delete_message(request.chat.id, request.message_id)
    bot.send_message(request.chat.id, f'Приветствую, {request.from_user.first_name}!', parse_mode='HTML')
    msg = bot.send_message(request.chat.id, f'Для продолжения работы введите: /menu', parse_mode='HTML')


@bot.message_handler(commands=["get_random_recipe"])
def bot_get_random_recipe(request):
    bot.delete_message(request.chat.id, request.message_id)
    rnd_recipe = get_random_recipe()
    bot.send_message(request.chat.id, f'***Рандомный рецепт - {rnd_recipe.title}.***', parse_mode='MARKDOWN')
    bot.send_message(request.chat.id, f'Автор рецепта: <i>{rnd_recipe.author.last_name} {rnd_recipe.author.first_name}</i>, никнейм - <b>{rnd_recipe.author.username}</b>', parse_mode='HTML')
    bot.send_message(request.chat.id, f'{rnd_recipe.text}', parse_mode='HTML')


@bot.message_handler(commands=['get_recipe'])
def bot_get_recipe(request, show=True):
    """Функция получения рецентов."""
    bot.delete_message(request.chat.id, request.message_id)
    params = request.text.replace('/get_recipe', '').lstrip()

    if params != "":
        try:
            parsed = parse_input(params)
        except WrongInputError:
            bot.send_message(request.chat.id, "Введены некорретные данные")
        else:
            result = get_recipe(parsed)
            show_result(bot, result, request)
    else:
        sent = bot.send_message(request.chat.id, f'Укажите <b>категорию</b>(обязательно), <b>тип</b>(опционально), <b>количество</b>(опционально) через звездочку. Пример: <b>супы*сырный суп*5</b>', parse_mode='HTML')

        show_available_cats_and_types(bot, request)

        bot.register_next_step_handler(sent, get_recipe)


@bot.message_handler(commands=['add_recipe'])
def bot_add_recipe(request):
    """Функция добавления рецентов."""
    bot.delete_message(request.chat.id, request.message_id)
    sent = bot.send_message(request.chat.id, f'Введите <b>категорию</b>, <b>тип</b>, <b>название</b> через звездочку. Все поля обязательные. Пример: <b>супы*сырный суп*название супа</b>', parse_mode='HTML')
    show_available_cats_and_types(bot, request)
    bot.register_next_step_handler(sent, bot_params_maker)


def bot_params_maker(request):
    """Функция получения параметров для рецепта."""
    recipe["params"] = request.text
    sent = bot.send_message(request.chat.id, f'Загрузите картинку:', parse_mode='HTML')
    bot.register_next_step_handler(sent, bot_get_photo)


def bot_get_photo(request):
    url = f"https://api.telegram.org/bot{SECRET_KEY}/getFile?file_id={request.photo[-1].file_id}"

    res = requests.get(url)

    file_path = json.loads(res.content)["result"]["file_path"]

    template = f"https://api.telegram.org/file/bot{SECRET_KEY}/{file_path}"

    res = requests.get(template)

    with open("tmp.png", "wb") as file:
        file.write(res.content)

    sent = bot.send_message(request.chat.id, f'Введите рецепт:', parse_mode='HTML')
    bot.register_next_step_handler(sent, bot_recipe_maker)

def bot_recipe_maker(self):
    """Функция создания рецентов."""

    try:
        parsed = parse_input(recipe["params"])
    except WrongInputError:
        bot.send_message(self.chat.id, "Введены некорретные данные")
    else:
        parsed["text"] = self.text
        parsed["author"] = validate_author_fields({"username": self.from_user.username, "first_name": self.from_user.first_name, "last_name": self.from_user.last_name})
        try:
            res = add_recipe(parsed)
            bot.send_message(self.chat.id, f'Рецепт успешно создан!', parse_mode='HTML')
        except WrongInputError:
            bot.send_message(self.chat.id, f'Введены некорретные данные.', parse_mode='HTML')


@bot.message_handler(commands=['menu'])
def bot_menu(request):
    """Функция получения списка доступных команд."""
    bot.delete_message(request.chat.id, request.message_id)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    kb.add(*[types.KeyboardButton(text=elem) for elem in commands])
    bot.send_message(request.chat.id, 'Доступные команды:', reply_markup=kb)


@bot.message_handler(func=lambda x: x not in commands)
def bot_wrong(request):
    """Функция ответа на некорретно введенную команду."""
    bot.reply_to(request, 'Введена некорретная команда.')




if __name__ == '__main__':
    start_bot()